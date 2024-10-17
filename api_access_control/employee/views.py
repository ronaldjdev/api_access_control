# import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from django.http import JsonResponse
# from django.contrib.auth import authenticate
# from jwt import encode

# from decouple import config
from .models import Employee

# import json 


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_card = data.get('id_card')
            password = data.get('password')

            # Buscar el empleado por identificación (o cualquier campo relevante)
            employee = Employee.objects.filter(id_card=id_card).first()

            if employee and employee.check_password(password):
                # Generar el token JWT utilizando RefreshToken

                refresh = RefreshToken.for_user(employee)
                print(employee)
                # Enviar la data adicional
                employee_data = {
                    'name': employee.name,
                    'id_card': employee.id_card,
                    'type_id_card': employee.get_type_id_card_display(),
                    'email': employee.email,
                    'image': employee.image.url if employee.image else None,
                    'phone': employee.phone,
                    'address': employee.address,
                    'marital_status': employee.get_marital_status_display(),
                    'gender': employee.get_gender_display(),
                    'rh': employee.get_rh_display(),
                    'role': employee.role,
                    'job': employee.job,
                }

                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'data': employee_data
                })

            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    print(f"User authenticated: {request.user.is_authenticated}")  # Debug print
    print(f"User ID: {request.user.id}")  # Debug print

    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()  # Invalida el token de refresh

        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)


    except ValueError as ve:
        return Response({"error": "Value Error: " + str(ve)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

     
# def sign_in(request):
#     """
#     Autenticar un empleado y devolver un token JWT para acceder a los endpoints protegidos.

#     El endpoint espera un JSON con los campos "id_card" y "password". Si el empleado existe y
#     la contraseña es correcta, se devuelve un token JWT en el campo "token". En caso contrario, se
#     devuelve un JSON con el campo "error" y un mensaje de error.

#     El token JWT tiene una duración de 1 hora y contiene el ID del empleado y su nombre.

#     El endpoint devuelve un estado 400 si el formato JSON es inválido o si las credenciales son
#     incorrectas. Si se utiliza un método distinto de POST, se devuelve un estado 405.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             id_card = data.get('id_card')
#             password = data.get('password')

#             # Buscar el empleado por identificación
#             employee = Employee.objects.filter(id_card=id_card).first()
#             if employee and employee.check_password(password):
#                 # Generar el token JWT
#                 payload = {
#                     # Convierte el UUID a string
#                     'employee_id': str(employee.id),
#                     'name': employee.name,
#                     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#                 }
#                 data = {
#                     'name': employee.name,
#                     'id_card': employee.id_card,
#                     'type_id_card': employee.get_type_id_card_display(),  # Descripción del choice
#                     'email': employee.email,
#                     'image': employee.image.url if employee.image else None,
#                     'phone': employee.phone,
#                     'address': employee.address,
#                     'marital_status': employee.get_marital_status_display(),  # Descripción del choice
#                     'gender': employee.get_gender_display(),  # Descripción del choice
#                     'rh': employee.get_rh_display(),  # Descripción del choice
#                     'role': employee.role,
#                     'job': employee.job,
#                 }

#                 token = encode(payload, config(
#                     'SECRET_KEY'), algorithm='HS256')
#                 return JsonResponse({
#                     'token': token,
#                     'data': data
#                 })

#             return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

#     return JsonResponse({'error': 'Método no permitido'}, status=405)
