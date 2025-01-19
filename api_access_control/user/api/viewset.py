from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from ..permissions import IsAdminOrSelf
from ..models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        """
        Modifica el queryset para que los usuarios regulares solo puedan
        ver su propio usuario, mientras que los administradores ven todo.
        """
        if self.request.user.is_staff:
            return User.objects.filter(is_active=True)
        return User.objects.filter(is_active=True, id=self.request.user.id)


    def destroy(self, request, pk=None, **kwargs):
        """
        Elimina un usuario desactivandolo. Los usuarios eliminados no se pueden
        recuperar. Solo los administradores pueden eliminar usuarios.

        Devuelve un objeto con la clave "detail" y el valor "Usuario eliminado
        correctamente." con un estatus 200.
        """
        try:
            user = self.get_object()
        except User.DoesNotExist:
            raise NotFound(detail="Usuario no encontrado.")
        user.is_active = False
        user.save()
        return Response({"detail": "Usuario eliminado correctamente."}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates a user's information. Validates and saves the provided data, then
        generates new access and refresh tokens for the updated user.

        Args:
            request: The HTTP request containing the partial data for the user update.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object containing the new access and refresh tokens, 
            along with the updated user data and a status of 200 OK.
        """

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