from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = User.objects.filter(is_active=True)

    def destroy (self, request, pk=None, **kwargs):
        data = self.get_queryset().filter(id=pk).first()
        if data:
            data.is_active = False
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)