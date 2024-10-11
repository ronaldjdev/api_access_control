import pyqrcode
import jwt
import os   
import datetime
from base.settings import SECRET_KEY

def generate_dynamic_qr(employee_id):
    """
    Genera un código QR dinámico para un empleado.

    Args:
        employee_id (uuid): Identificador del empleado.

    Returns:
        str: Ruta del archivo del código QR generado.

    El código QR contiene un token JWT que lleva el identificador del empleado y
    una marca de tiempo. El token es válido por 5 minutos.
    """
    qr_directory = 'media/qr'
    
    # Asegúrate de que la carpeta existe
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)

    timestamp = datetime.datetime.now().isoformat()
    payload = {
        'employee_id': employee_id,
        'timestamp': timestamp,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # QR válido por 5 minutos
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # Crea el QR y guarda en la ruta correcta
    qr = pyqrcode.create(token, error='L')
    qr_filename = f'{employee_id}_qr.png'
    qr_path = os.path.join(qr_directory, qr_filename)
    
    qr.png(qr_path, scale=8)  # Guarda el QR en la ruta correcta

    return qr_path  # Devuelve la ruta completa del archivo QR
