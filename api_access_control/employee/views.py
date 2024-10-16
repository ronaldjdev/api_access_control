import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jwt import encode

from base.settings import SECRET_KEY
from .models import Employee




@csrf_exempt
def sign_in(request):
    """
    Autenticar un empleado y devolver un token JWT para acceder a los endpoints protegidos.

    El endpoint espera un JSON con los campos "id_card" y "password". Si el empleado existe y
    la contraseña es correcta, se devuelve un token JWT en el campo "token". En caso contrario, se
    devuelve un JSON con el campo "error" y un mensaje de error.

    El token JWT tiene una duración de 1 hora y contiene el ID del empleado y su nombre.

    El endpoint devuelve un estado 400 si el formato JSON es inválido o si las credenciales son
    incorrectas. Si se utiliza un método distinto de POST, se devuelve un estado 405.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_card = data.get('id_card')
            password = data.get('password')

            # Buscar el empleado por identificación
            employee = Employee.objects.filter(id_card=id_card).first()
            if employee and employee.check_password(password):
                # Generar el token JWT
                payload = {
                    'employee_id': str(employee.id),  # Convierte el UUID a string
                    'name': employee.name,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                token = encode(payload, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'token': token})

            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



