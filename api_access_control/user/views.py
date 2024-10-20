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
from .models import User

# import json 


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_card = data.get('id_card')
            password = data.get('password')

            # Buscar el empleado por identificación (o cualquier campo relevante)
            user = User.objects.filter(id_card=id_card).first()

            if user and user.check_password(password):
                # Generar el token JWT utilizando RefreshToken

                refresh = RefreshToken.for_user(user)
                print(user)
                # Enviar la data adicional
                employee_data = {
                    'name': user.name,
                    'id_card': user.id_card,
                    'type_id_card': user.get_type_id_card_display(),
                    'email': user.email,
                    'image': user.employee.image.url if user.image else None,
                    'phone': user.phone,
                    'address': user.address,
                    'marital_status': user.get_marital_status_display(),
                    'gender': user.get_gender_display(),
                    'rh': user.get_rh_display(),
                    'role': user.role,
                    'job': user.job,
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
