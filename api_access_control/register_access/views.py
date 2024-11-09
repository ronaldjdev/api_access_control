import os

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import RegisterAccess
# from base.settings import SECRET_KEY
# from employee.models import Employee
from user.models import User
# from .utils.qr_reader import read_qr_camera
from .utils.qr_generator import generate_dynamic_qr, generate_qr_view

def decode_token(token):
    try:
        # Validar y decodificar el token usando UntypedToken
        decoded = AccessToken(token)
        return decoded.payload  # Retorna el payload del token
    except TokenError as e:
        # Lanza la excepción para que la maneje el except en verify_qr
        raise InvalidToken("Token inválido o expirado") from e  
    
    
@csrf_exempt
def verify_qr(request):
    
    if request.method == "POST":
        qr_data = request.POST.get('qr_data')
        if qr_data:
            try:
                decoded = decode_token(qr_data)
                user_id = decoded['use_id']
                user = User.objects.get(id=user_id)

                # Obtener el último registro de acceso
                last_register = RegisterAccess.objects.filter(user=user).last()

                if last_register is None or last_register.type_access == 'OUT':
                    # Si no hay registros o el último es OUT, se crea un nuevo registro de entrada
                    type_access = 'IN'
                    new_register = RegisterAccess.objects.create(user=user, type_access=type_access, qr_data=qr_data, user_entry=timezone.now())
                    return JsonResponse({
                        'status': 'success', 
                        'type_access': type_access, 
                        'entry_time': new_register.user_entry.isoformat(),
                        'message': 'Acceso verificado',
                        })
                elif last_register.type_access == 'IN':
                    # Si el último registro es IN, se actualiza el registro para marcar la salida
                    last_register.user_exit = timezone.now()  # Asumiendo que has importado timezone
                    last_register.type_access = 'OUT'
                    last_register.save()

                    return JsonResponse({
                        'status': 'success', 
                        'type_access': 'OUT', 
                        'exit_time': last_register.user_exit.isoformat()
                        })
                
                return JsonResponse({'status': 'success', 'type_access': type_access})
            
            except InvalidToken:
                return JsonResponse({'status': 'error', 'message': 'QR inválido'}, status=400)
            except TokenError as e:
                # Esto captura otros errores de token como expirado
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

    
  

# @csrf_exempt
# def verify_qr_from_camera(request):
#     """
#     Verifica un código QR escaneado desde la cámara en tiempo real.
#     """

#     qr_data = read_qr_camera()
#     if not qr_data:
#         return JsonResponse({'status': 'error', 'message': 'No se encontró un QR válido'})

#     # Verificar el contenido del QR escaneado
#     try:
#         decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
#         employee_id = decoded['employee_id']
#         employee = Employee.objects.get(id=employee_id)

#         # Obtener el último registro de acceso
#         last_register = RegisterAccess.objects.filter(employee=employee).last()

#         if last_register is None or last_register.type_access == 'OUT':
#             # Si no hay registros o el último es OUT, se crea un nuevo registro de entrada
#             type_access = 'IN'
#             new_register = RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data, employee_entry=timezone.now())
#             return JsonResponse({'status': 'success', 'type_access': type_access, 'entry_time': new_register.employee_entry.isoformat()})
#         elif last_register.type_access == 'IN':
#             # Si el último registro es IN, se actualiza el registro para marcar la salida
#             last_register.employee_exit = timezone.now()  # Asumiendo que has importado timezone
#             last_register.type_access = 'OUT'
#             last_register.save()

#             return JsonResponse({'status': 'success', 'type_access': 'OUT', 'exit_time': last_register.employee_exit.isoformat()})


#         return JsonResponse({'status': 'success', 'type_access': type_access})
#     except jwt.ExpiredSignatureError:
#         return JsonResponse({'status': 'error', 'message': 'QR expirado'})
#     except jwt.InvalidTokenError:
#         return JsonResponse({'status': 'error', 'message': 'QR inválido'})


def generate_qr_from_employee(request):
    """
    Endpoint para generar un código QR dinámico para un empleado.
    """
    
    token = request.META.get('HTTP_AUTHORIZATION')  
    if not token:
        return JsonResponse({'status': 'error', 'message': 'Token no proporcionado'}, status=403)

    try:
        token = token.split()[1]  # Extraer solo el token
        payload = decode_token(token)
        user_id = payload['user_id']  # Extraer el ID del empleado
    except (TokenError, InvalidToken) as e:
        return JsonResponse({'status': 'error', 'message': 'Token inválido', 'error': str(e)}, status=403)
    
    # Generar el QR para el empleado
    qr_path = generate_dynamic_qr(user_id)
    
    if not qr_path:
        return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado'})
    
    # Devolver la ruta o URL del QR generado
    qr_url = f'media/qr/{os.path.basename(qr_path)}'  # Suponiendo que las imágenes están servidas desde /media/
    return JsonResponse({'status': 'success', 'qr_image_url': qr_url})

@csrf_exempt
def generate_qr_temporary(request):
    """
    Endpoint para generar un código QR dinámico para un empleado.
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    print('token: ', token)  
    if not token:
        return JsonResponse({'status': 'error', 'message': 'Token no proporcionado'}, status=403)

    try:
        token = token.split()[1]  # Extraer solo el token
        payload = decode_token(token)
        user_id = payload['user_id']  # Extraer el ID del empleado
        print('payload: ', payload)
    except (TokenError, InvalidToken) as e:
        return JsonResponse({'status': 'error', 'message': 'Token inválido', 'error': str(e)}, status=403)
    
    # Generar el QR para el empleado y devolverlo como una imagen directamente
    return generate_qr_view(user_id)