from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
import datetime

from base.settings import SECRET_KEY

from .models import Employee



@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identification = data.get('identification')
            password = data.get('password')

            # Buscar el empleado por identificación
            empleado = Employee.objects.filter(identification=identification).first()
            if empleado and empleado.check_password(password):
                # Generar el token JWT
                payload = {
                    'employee_id': str(empleado.id),  # Convierte el UUID a string
                    'name': empleado.name,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'token': token})

            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
