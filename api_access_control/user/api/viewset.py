from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def destroy(self, request, pk=None, **kwargs):
        # Utiliza `get_object_or_404` o `get_object` para mayor claridad
        try:
            user = self.get_object()
        except User.DoesNotExist:
            raise NotFound(detail="Usuario no encontrado.")
        user.is_active = False
        user.save()
        return Response({"detail": "Usuario eliminado correctamente."}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        """Actualiza parcialmente un usuario y retorna tokens."""
        instance = self.get_object()  # Obtiene el usuario
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Genera los tokens usando SimpleJWT
        refresh = RefreshToken.for_user(instance)

        # Construye la respuesta
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)