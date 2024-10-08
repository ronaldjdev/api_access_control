import threading
import time

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import jwt

from .models import RegisterAccess
from base.settings import SECRET_KEY
from employee.models import Employee
from .utils.qr_reader import read_qr_image, read_qr_camera, qr_data_global
from .utils.qr_generator import generate_dynamic_qr

def read_qr_from_image(request):
    # Suponiendo que recibes una imagen del QR como parte de la solicitud
    image_path = request.FILES['image'].temporary_file_path()
    
    # Leer el QR desde la imagen
    qr_data = read_qr_image(image_path)
    if not qr_data:
        return JsonResponse({'status': 'error', 'message': 'No se encontró un QR válido'})

    # Verificar el QR escaneado
    try:
        decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
        employee_id = decoded['employee_id']
        employee = Employee.objects.get(id=employee_id)

        # Determinar si es entrada o salida
        last_register = RegisterAccess.objects.filter(employee=employee).last()
        type_access = 'IN' if last_register is None or last_register.type_access == 'OUT' else 'OUT'

        # Registrar el acceso
        RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data)

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
    threading.Thread(target=read_qr_camera, daemon=True).start()
    time.sleep(5)
    # Obtener el contenido del QR escaneado
    qr_data = qr_data_global
    print("QR DATA: ",qr_data)
    if not qr_data:
        return JsonResponse({'status': 'error', 'message': 'No se encontró un QR válido'})

    # Verificar el contenido del QR escaneado
    try:
        decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
        employee_id = decoded['employee_id']
        employee = Employee.objects.get(id=employee_id)

        # Determinar si es entrada o salida
        last_register = RegisterAccess.objects.filter(employee=employee).last()
        type_access = 'IN' if last_register is None or last_register.type_access == 'OUT' else 'OUT'

        # Registrar el acceso
        RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data)

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
    qr_filename = generate_dynamic_qr(employee_id)
    
    if not qr_filename:
        return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado'})
    
    # Devolver la ruta o URL del QR generado
    qr_url = f'/media/{qr_filename}'  # Suponiendo que las imágenes están servidas desde /media/
    return JsonResponse({'status': 'success', 'qr_image_url': qr_url})
