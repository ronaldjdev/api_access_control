from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permite que los usuarios accedan solo a empleados asociados a ellos mismos.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica si el usuario autenticado es el propietario del empleado.

        Args:
            request (rest_framework.request.Request): La solicitud HTTP.
            view (rest_framework.viewsets.ModelViewSet): La vista que maneja la solicitud.
            obj (api_access_control.employee.models.Employee): El objeto de empleado a verificar.

        Returns:
            bool: Verdadero si el usuario autenticado es el propietario del empleado, Falso en caso contrario.
        """
        return obj.user == request.user
