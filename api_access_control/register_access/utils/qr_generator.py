import pyqrcode
# import qrcode
import jwt
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
    
    timestamp = datetime.datetime.now().isoformat()
    payload = {
        'employee_id': employee_id,
        'timestamp': timestamp,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # QR válido por 5 minutos
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    qr = pyqrcode.create(token,error='L')
    qr.png(f'{employee_id}_qr.png', scale=8)

    return f'{employee_id}_qr.png'
