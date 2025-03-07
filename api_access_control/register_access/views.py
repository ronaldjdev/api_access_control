import os
import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import RegisterAccess
from user.models import User
from .utils.qr_generator import generate_dynamic_qr, generate_dynamic_qr_view
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
def decode_token(token):
    """
    Decodifica un token y devuelve su payload.

    Args:
        token (str): El token a decodificar.

    Returns:
        dict: El payload del token decodificado.

    Raises:
        InvalidToken: Si el token es inválido o expirado.
    """

    try:
        # Validar y decodificar el token usando UntypedToken
        decoded = AccessToken(token)
        return decoded.payload  # Retorna el payload del token
    except TokenError as e:
        # Lanza la excepción para que la maneje el except en verify_qr
        raise InvalidToken("Token inválido o expirado") from e

@csrf_exempt
def verify_qr(request):
    """
    Verifica un código QR y registra el acceso de un usuario.

    Verifica si el código QR proporcionado es válido y corresponde a un usuario existente.
    Si el último registro de acceso del usuario es "OUT" o no existe, crea un nuevo registro "IN".
    Si el último registro de acceso del usuario es "IN", marca la salida y actualiza el registro.

    Devuelve una respuesta JSON con el tipo de acceso ("IN" o "OUT"), el horario de acceso o salida y un mensaje.

    Args:
        request (HttpRequest): La solicitud HTTP entrante.

    Returns:
        JsonResponse: Una respuesta JSON con el tipo de acceso, horario y mensaje.

    Raises:
        TokenError: Si el token proporcionado no es válido o ha expirado.
        InvalidToken: Si el token proporcionado no es un token JWT válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        qr_data = data.get("qr_data")
        print("qr_data:", qr_data)
        remark = data.get("remark", "")
        print("remark:", remark)

        if not qr_data:
            return JsonResponse({"status": "error", "message": "QR no proporcionado"}, status=400)

        if qr_data:
            try:
                decoded = decode_token(qr_data)
                print("QR decodificado correctamente:", decoded)
                user_id = decoded["user_id"]
                user = User.objects.get(id=user_id)

                # Obtener el primer registro con tipo de acceso "IN"
                register_type = RegisterAccess.objects.filter(user=user, type_access="IN").first()

                if register_type:
                    # Si el primer registro "IN" existe, marcar la salida
                    register_type.user_exit = timezone.now()
                    register_type.type_access = "OUT"
                    new_remark = {**register_type.remark, "exit_observation": remark or ""}  # Asegúrate de que remark no sea None
                    register_type.remark = new_remark
                    register_type.save()

                    return JsonResponse(
                        {
                            "status": "success",
                            "name": user.name + " " + user.last_name,
                            "type_access": "OUT",
                            "exit_time": register_type.user_exit.isoformat(),
                            "message": "Salida confirmada",
                        }
                    )

                # Si no hay registro "IN", o el último registro es "OUT", se crea un nuevo registro "IN"
                type_access = "IN"
                new_remark = {"entry_observation": remark or ""}
                new_register = RegisterAccess.objects.create(
                    user=user,
                    type_access=type_access,
                    remark=new_remark,
                    qr_data=qr_data,
                    user_entry=timezone.now(),
                )
                return JsonResponse(
                    {
                        "status": "success",
                        "name": user.name + " " + user.last_name,
                        "type_access": type_access,
                        "entry_time": new_register.user_entry.isoformat(),
                        "message": "Acceso confirmado",
                    }
                )

            except InvalidToken as e:
                print("Error al decodificar QR:", e)
                return JsonResponse({"status": "error", "message": "QR inválido"}, status=400)
            except TokenError as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Usuario no encontrado"}, status=404)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

def generate_qr_from_employee(request):
    """
    Genera un código QR dinámico para un empleado, utilizando el token de autenticación
    proporcionado en el encabezado HTTP_AUTHORIZATION.

    Devuelve una respuesta JSON con la ruta o URL del archivo QR generado, o un mensaje de error
    si el token no es válido o no se encuentra el empleado.

    Devoluciones:
        JsonResponse: una respuesta JSON con la ruta del archivo QR o un mensaje de error.

    Sube:
        TokenError: si el token proporcionado no es válido o ha expirado.
        InvalidToken: si el token proporcionado no es un token JWT válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.
    """

    token = request.META.get("HTTP_AUTHORIZATION")
    if not token:
        return JsonResponse(
            {"status": "error", "message": "Token no proporcionado"}, status=403
        )

    try:
        token = token.split()[1]
        payload = decode_token(token)
        user_id = payload["user_id"]
    except (TokenError, InvalidToken) as e:
        return JsonResponse(
            {"status": "error", "message": "Token inválido", "error": str(e)},
            status=403,
        )

    qr_path = generate_dynamic_qr(user_id)

    if not qr_path:
        return JsonResponse({"status": "error", "message": "Empleado no encontrado"})

    qr_url = f"media/qr/{os.path.basename(qr_path)}"
    return JsonResponse({"status": "success", "qr_image_url": qr_url})


@csrf_exempt
def generate_qr_temporary(request):
    """
    Genera un código QR dinámico para un empleado, utilizando el token de autenticación
    proporcionado en el encabezado HTTP_AUTHORIZATION.

    Devuelve una respuesta HTTP con el código QR generado como una imagen PNG.

    Argumentos:
        solicitud (HttpRequest): la solicitud HTTP entrante que contiene el token de autenticación.

    Devoluciones:
        HttpResponse: una respuesta HTTP con el código QR generado como una imagen PNG.

    Sube:
        TokenError: si el token proporcionado no es válido o ha expirado.
        InvalidToken: si el token proporcionado no es un token JWT válido.
        User.DoesNotExist: Si el usuario asociado al token no existe.
    """

    token = request.META.get("HTTP_AUTHORIZATION")
    if not token:
        return JsonResponse(
            {"status": "error", "message": "Token no proporcionado"}, status=403
        )

    try:
        token = token.split()[1]  # Extraer solo el token
        payload = decode_token(token)
        user_id = payload["user_id"]  # Extraer el ID del empleado
    except (TokenError, InvalidToken) as e:
        return JsonResponse(
            {"status": "error", "message": "Token inválido", "error": str(e)},
            status=403,
        )

    # Generar el QR para el empleado y devolverlo como una imagen directamente
    return generate_dynamic_qr_view(user_id)
