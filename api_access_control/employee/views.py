from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import jwt
import datetime

from base.settings import SECRET_KEY
from .models import Employee


@csrf_exempt
def sign_in(request):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    """
    if request.method == 'POST':
        identification = request.POST.get('identification')
        password = request.POST.get('password')

        # Buscar empleado por identificación
        empleado = get_object_or_404(Employee, identification=identification)

        # Verificar la contraseña
        if empleado.check_password(password):
            # Generar el token JWT
            payload = {
                'employee_id': empleado.id,
                'name': empleado.name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
