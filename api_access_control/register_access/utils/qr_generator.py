from io import BytesIO
import pyqrcode
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import AccessToken
from user.models import User

def generate_dynamic_qr(user_id):
    """
    Genera un código QR en memoria dinámicamente para un usuario.

    Args:
        user_id (uuid): El ID del usuario para el cual se generará el QR.

    Returns:
        BytesIO: Un buffer de BytesIO que contiene el QR en formato PNG.

    Raises:
        ValueError: Si no existe un usuario con el ID proporcionado.
    """
    try:
        user = User.objects.get(id=user_id)  # Obtén el objeto de usuario
    except User.DoesNotExist:
        raise ValueError("Usuario no encontrado")

    token = str(AccessToken.for_user(user))  # Genera el token para el usuario
    
    # Crea el código QR en memoria (usando un buffer de BytesIO)
    qr = pyqrcode.create(token, error='L')
    buffer = BytesIO()
    qr.png(buffer, scale=8)  # Guarda el QR en el buffer
    buffer.seek(0)  # Resetea el puntero del buffer al inicio

    return buffer  # Devuelve el buffer con el QR



def generate_dynamic_qr_view(user_id):
    """
    Genera y devuelve un código QR en formato de imagen PNG para un usuario específico.

    Args:
        user_id (uuid): El ID del usuario para el cual se generará el código QR.

    Returns:
        HttpResponse: Una respuesta HTTP que contiene la imagen PNG del código QR.

    Raises:
        ValueError: Si no existe un usuario con el ID proporcionado.
    """
    try:
        user = User.objects.get(id=user_id)  
    except User.DoesNotExist:
        raise ValueError("Usuario no encontrado")

    token = str(AccessToken.for_user(user))  
    qr = pyqrcode.create(token, error='L')
    
    # Crea un buffer de memoria para almacenar la imagen
    buffer = BytesIO()
    qr.png(buffer, scale=8)  
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")
