from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import User

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intentar autenticar usando el username
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # Intentar autenticar usando id_card
            try:
                id_card = int(username)  # Convierte a entero para la comparación
                user = User.objects.get(id_card=id_card)
            except ObjectDoesNotExist:
                return None
        
        # Verifica la contraseña
        if user.check_password(password):
            return user
        
        return None
