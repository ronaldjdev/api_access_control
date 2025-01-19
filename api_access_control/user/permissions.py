from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrSelf(BasePermission):
    """
    Permite acceso completo a los administradores.
    Los usuarios regulares pueden editar y ver solo su propia información.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica si el usuario autenticado tiene permiso para acceder al objeto.
        
        Args:
            request (rest_framework.request.Request): La solicitud HTTP.
            view (rest_framework.viewsets.ModelViewSet): La vista que maneja la solicitud.
            obj (api_access_control.user.models.User): El objeto de usuario a verificar.
        
        Returns:
            bool: Verdadero si el usuario autenticado tiene permiso para acceder al objeto, Falso en caso contrario.
        """
        if request.user.is_staff:
            return True
        # Los usuarios autenticados pueden ver y editar solo su propio perfil
        return obj == request.user
