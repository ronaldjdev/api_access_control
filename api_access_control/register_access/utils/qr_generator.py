import os

import pyqrcode
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from user.models import User

@permission_classes([IsAuthenticated])
def generate_dynamic_qr(user_id):

    print('user id: ',user_id)

    qr_directory = 'base/media/qr'
    
    # Asegúrate de que la carpeta existe
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)
    # Obtén el usuario usando el user_id
    try:
        user = User.objects.get(id=user_id)  # Obtén el objeto de usuario
    except User.DoesNotExist:
        raise ValueError("Usuario no encontrado")

    token = str(RefreshToken.for_user(user))

    print(token)

    # Crea el QR y guarda en la ruta correcta
    qr = pyqrcode.create(token, error='L')
    qr_filename = f'{user_id}_qr.png'
    qr_path = os.path.join(qr_directory, qr_filename)
    
    qr.png(qr_path, scale=8)  # Guarda el QR en la ruta correcta

    return qr_path  # Devuelve la ruta completa del archivo QR
