import os

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import RegisterAccess
from user.models import User
from .utils.qr_generator import generate_dynamic_qr, generate_dynamic_qr_view

def decode_token(token):
    """
    Decodifica un token y devuelve su payload.

    Args:
        token (str): El token a decodificar.

    Returns:
        dict: El payload del token decodificado.

    Raises:
        InvalidToken: Si el token es inválido o expirado.
    """

    try:
        # Validar y decodificar el token usando UntypedToken
        decoded = AccessToken(token)
        return decoded.payload  # Retorna el payload del token
    except TokenError as e:
        # Lanza la excepción para que la maneje el except en verify_qr
        raise InvalidToken("Token inválido o expirado") from e  
    
@csrf_exempt
def verify_qr(request):
    """
    Verifica un código QR decodificando sus datos y actualizando el registro de acceso del usuario.

    Esta vista maneja solicitudes POST que contienen datos QR. Decodifica los datos para 
    recupera la información del usuario y actualiza el registro de acceso del usuario. 
    Si el último registro de acceso es 'OUT' o no existe ninguno, se crea un nuevo registro 'IN'. 
    Si el último registro es 'IN', actualiza el registro a 'OUT' con el registro actual 
    marca de tiempo.

    Argumentos:
    solicitud (HttpRequest): la solicitud HTTP entrante que contiene datos QR.

    Devoluciones:
        JsonResponse: una respuesta JSON que indica el éxito o el fracaso de la 
        proceso de verificación, junto con el tipo de acceso y la marca de tiempo si tiene éxito.

    Sube:
        InvalidToken: si los datos QR contienen un token no válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.

    """
    
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

def generate_qr_from_employee(request):
    """
    Genera un código QR dinámico para un empleado, utilizando el token de autenticación 
    proporcionado en el encabezado HTTP_AUTHORIZATION.

    Devuelve una respuesta JSON con la ruta o URL del archivo QR generado, o un mensaje de error 
    si el token no es válido o no se encuentra el empleado.

    Devoluciones:
        JsonResponse: una respuesta JSON con la ruta del archivo QR o un mensaje de error.

    Sube:
        TokenError: si el token proporcionado no es válido o ha expirado.
        InvalidToken: si el token proporcionado no es un token JWT válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.
    """

    token = request.META.get('HTTP_AUTHORIZATION')  
    if not token:
        return JsonResponse({'status': 'error', 'message': 'Token no proporcionado'}, status=403)

    try:
        token = token.split()[1]  
        payload = decode_token(token)
        user_id = payload['user_id']  
    except (TokenError, InvalidToken) as e:
        return JsonResponse({'status': 'error', 'message': 'Token inválido', 'error': str(e)}, status=403)
    
  
    qr_path = generate_dynamic_qr(user_id)
    
    if not qr_path:
        return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado'})
    
  
    qr_url = f'media/qr/{os.path.basename(qr_path)}'  
    return JsonResponse({'status': 'success', 'qr_image_url': qr_url})

@csrf_exempt
def generate_qr_temporary(request):
    """
    Genera un código QR dinámico para un empleado, utilizando el token de autenticación 
    proporcionado en el encabezado HTTP_AUTHORIZATION.

    Devuelve una respuesta HTTP con el código QR generado como una imagen PNG.

    Argumentos:
        solicitud (HttpRequest): la solicitud HTTP entrante que contiene el token de autenticación.

    Devoluciones:
        HttpResponse: una respuesta HTTP con el código QR generado como una imagen PNG.

    Sube:
        TokenError: si el token proporcionado no es válido o ha expirado.
        InvalidToken: si el token proporcionado no es un token JWT válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.
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
    return generate_dynamic_qr_view(user_id)