from io import BytesIO
import pyqrcode

from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

def generate_dynamic_qr(user_id):
    try:
        user = User.objects.get(id=user_id)  # Obtén el objeto de usuario
    except User.DoesNotExist:
        raise ValueError("Usuario no encontrado")

    token = str(RefreshToken.for_user(user))  # Genera el token para el usuario
    
    # Crea el código QR en memoria (usando un buffer de BytesIO)
    qr = pyqrcode.create(token, error='L')
    buffer = BytesIO()
    qr.png(buffer, scale=8)  # Guarda el QR en el buffer
    buffer.seek(0)  # Resetea el puntero del buffer al inicio

    return buffer  # Devuelve el buffer con el QR
