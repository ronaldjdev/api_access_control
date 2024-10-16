from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import RegisterAccess
from .serializers import RegisterAccessSerializer


class RegisterAccessViewSet(ModelViewSet):
    serializer_class = RegisterAccessSerializer
    queryset = RegisterAccess.objects.filter(is_active=True)

    def destroy (self, request, pk=None, **kwargs):
        data = self.get_queryset().filter(id=pk).first()
        if data:
            data.is_active = False
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)