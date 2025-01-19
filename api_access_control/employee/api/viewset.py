from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Employee
from ..permissions import IsOwner
from .serializers import EmployeeSerializer

class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsOwner]
    # lookup_field = 'id'
    
    def get_queryset(self):
        """
        Modifica el queryset para que los usuarios regulares solo puedan
        ver sus propios empleados, mientras que los administradores ven todo.
        """
        
        return Employee.objects.filter(user=self.request.user)
    
    def destroy (self, request, pk=None, **kwargs):
        """
        Deactivate an employee by setting its 'is_active' status to False.
        
        Args:
            request (rest_framework.request.Request): The HTTP request object.
            pk (str): The primary key of the employee to be deactivated.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object with HTTP 200 status if successful,
            or HTTP 400 status if the employee is not found.
        """

        data = self.get_queryset().filter(id=pk).first()
        if data:
            data.is_active = False
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)