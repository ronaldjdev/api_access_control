import pyqrcode
import jwt
import datetime

from base.settings import SECRET_KEY


def generate_dynamic_qr(employee_id):
    timestamp = datetime.datetime.now().isoformat()
    payload = {
        'employee_id': employee_id,
        'timestamp': timestamp,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # QR válido por 5 minutos
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    qr = pyqrcode.create(token)
    qr.png(f'{employee_id}_qr.png', scale=5)
    return f'{employee_id}_qr.png'
