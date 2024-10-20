import os

from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import jwt

from .models import RegisterAccess
from base.settings import SECRET_KEY
from employee.models import Employee
from .utils.qr_reader import read_qr_camera
from .utils.qr_generator import generate_dynamic_qr


@csrf_exempt
def verify_qr(request):
    
    if request.method == "POST":
        qr_data = request.POST.get('qr_data')
        if qr_data:
            try:
                decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
                employee_id = decoded['employee_id']
                employee = Employee.objects.get(id=employee_id)

                # Obtener el último registro de acceso
                last_register = RegisterAccess.objects.filter(employee=employee).last()

                if last_register is None or last_register.type_access == 'OUT':
                    # Si no hay registros o el último es OUT, se crea un nuevo registro de entrada
                    type_access = 'IN'
                    new_register = RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data, employee_entry=timezone.now())
                    return JsonResponse({
                        'status': 'success', 
                        'type_access': type_access, 
                        'entry_time': new_register.employee_entry.isoformat(),
                        'message': 'Acceso verificado',
                        })
                elif last_register.type_access == 'IN':
                    # Si el último registro es IN, se actualiza el registro para marcar la salida
                    last_register.employee_exit = timezone.now()  # Asumiendo que has importado timezone
                    last_register.type_access = 'OUT'
                    last_register.save()

                    return JsonResponse({
                        'status': 'success', 
                        'type_access': 'OUT', 
                        'exit_time': last_register.employee_exit.isoformat()
                        })
                
                return JsonResponse({'status': 'success', 'type_access': type_access})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'status': 'error', 'message': 'QR expirado'})
            except jwt.InvalidTokenError:
                return JsonResponse({'status': 'error', 'message': 'QR inválido'})
    
  

@csrf_exempt
def verify_qr_from_camera(request):
    """
    Verifica un código QR escaneado desde la cámara en tiempo real.
    """

    qr_data = read_qr_camera()
    print("QR DATA: ",qr_data)
    if not qr_data:
        return JsonResponse({'status': 'error', 'message': 'No se encontró un QR válido'})

    # Verificar el contenido del QR escaneado
    try:
        decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
        employee_id = decoded['employee_id']
        employee = Employee.objects.get(id=employee_id)

        # Obtener el último registro de acceso
        last_register = RegisterAccess.objects.filter(employee=employee).last()

        if last_register is None or last_register.type_access == 'OUT':
            # Si no hay registros o el último es OUT, se crea un nuevo registro de entrada
            type_access = 'IN'
            new_register = RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data, employee_entry=timezone.now())
            return JsonResponse({'status': 'success', 'type_access': type_access, 'entry_time': new_register.employee_entry.isoformat()})
        elif last_register.type_access == 'IN':
            # Si el último registro es IN, se actualiza el registro para marcar la salida
            last_register.employee_exit = timezone.now()  # Asumiendo que has importado timezone
            last_register.type_access = 'OUT'
            last_register.save()

            return JsonResponse({'status': 'success', 'type_access': 'OUT', 'exit_time': last_register.employee_exit.isoformat()})


        return JsonResponse({'status': 'success', 'type_access': type_access})
    except jwt.ExpiredSignatureError:
        return JsonResponse({'status': 'error', 'message': 'QR expirado'})
    except jwt.InvalidTokenError:
        return JsonResponse({'status': 'error', 'message': 'QR inválido'})
    
def generate_qr_from_employee(request):
    """
    Endpoint para generar un código QR dinámico para un empleado.
    """
    
    token = request.META.get('HTTP_AUTHORIZATION')  # Obtener el token del encabezado
    print('Token recibido:', token)  # Imprimir el token recibido
    if not token:
        return JsonResponse({'status': 'error', 'message': 'Token no proporcionado'}, status=403)

    try:
        token = token.split()[1]  # Extraer solo el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # Decodificar el token
        print('Payload: ', payload)  # Imprimir el payload decodificado
        employee_id = payload['employee_id']  # Extraer el ID del empleado
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print('Error al decodificar el token:', str(e))  # Imprimir el error si hay uno
        return JsonResponse({'status': 'error', 'message': 'Token inválido'}, status=403)

    print('Employee ID: ', employee_id)
    
    # Generar el QR para el empleado
    qr_path = generate_dynamic_qr(employee_id)
    
    if not qr_path:
        return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado'})
    
    # Devolver la ruta o URL del QR generado
    qr_url = f'media/qr/{os.path.basename(qr_path)}'  # Suponiendo que las imágenes están servidas desde /media/
    return JsonResponse({'status': 'success', 'qr_image_url': qr_url})
