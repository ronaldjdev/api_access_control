from django.conf import settings
from django.core.files import File
import os
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from register_access.utils.qr_generator import generate_dynamic_qr

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
        user = request.user

        if not user or user.is_anonymous:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Buscar si ya existe un QR para el usuario
            existing_qr_code = QrCode.objects.filter(user=user).first()

            # Si ya existe un QR, eliminar el archivo anterior
            if existing_qr_code and existing_qr_code.qr_code:
                old_file_path = os.path.join(settings.MEDIA_ROOT, existing_qr_code.qr_code.name)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)  # Eliminar el archivo anterior


            # Generar un nuevo QR (solo el buffer)
            qr_buffer = generate_dynamic_qr(user.id)

            # Guardar el QR en la base de datos
            if existing_qr_code:
                # Si ya existe, actualizamos el archivo QR
                existing_qr_code.qr_code.save(f'{user.id}.png', File(qr_buffer), save=True)
                qr_code_instance = existing_qr_code
            else:
                # Si no existe, creamos uno nuevo
                qr_code_instance = QrCode(user=user)
                qr_code_instance.qr_code.save(f'{user.id}.png', File(qr_buffer), save=True)

            serializer = self.get_serializer(qr_code_instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def destroy (self, request, pk=None, **kwargs):
        data = self.get_queryset().filter(id=pk).first()
        if data:
            data.is_active = False
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
