from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .api.serializers import SignInSerializer, LogoutSerializer, TokenRefreshSerializer, RegisterSerializer, TokenVerifySerializer, EmailSerializer

class SignInView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class TokenVerifyView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación para verificación del token

    def post(self, request):
        serializer = TokenVerifySerializer(data=request.data)
        
        # Valida el serializador y devuelve si es válido o no
        if serializer.is_valid():
            return Response({"is_valid": True}, status=status.HTTP_200_OK)
        return Response({"is_valid": False, "errors": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)

class SendEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            recipient = serializer.validated_data['recipient']
            
            send_mail(
                subject,
                message,
                'info.nikaacc@gmail.com',  # Cambia este correo por el tuyo
                [recipient],
                fail_silently=False,
            )
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)