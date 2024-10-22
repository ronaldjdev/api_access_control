from io import BytesIO

from django.core.files import File

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import pyqrcode

from .serializers import RegisterAccessSerializer, GenerateQrCodeSerializer
from ..models import RegisterAccess, QrCode


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

class GenerateQrCodeViewSet(ModelViewSet):
    queryset = QrCode.objects.all()
    serializer_class = GenerateQrCodeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user  # Obtén el usuario autenticado

        # Crear el token de acceso para el usuario
        token = str(RefreshToken.for_user(user))

        # Generar el código QR
        qr = pyqrcode.create(token, error='L')

        # Crear un buffer para almacenar la imagen en memoria
        buffer = BytesIO()
        qr.png(buffer, scale=8)  # Guarda el QR en el buffer

        # Crear la instancia de QrCode
        qr_code_instance = QrCode(
            user=user,
        )

        # Asignar el archivo desde el buffer al campo `qr_code`
        qr_filename = f'{user.id}_qr.png'
        qr_code_instance.qr_code.save(qr_filename, File(buffer), save=True)

        # Serializa el código QR generado
        serializer = self.get_serializer(qr_code_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy (self, request, pk=None, **kwargs):
        data = self.get_queryset().filter(id=pk).first()
        if data:
            data.is_active = False
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
