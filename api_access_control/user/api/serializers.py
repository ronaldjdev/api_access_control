from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from employee.models import Employee
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'last_login',
            'timestamp',
            'created_at',
            'groups',
            'user_permissions',
            ]

    # Sobrescribe para manejar la contraseña
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.id_card = validated_data.get('id_card', instance.id_card)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class SignInSerializer(serializers.Serializer):
    id_card = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        id_card = data.get('id_card')
        password = data.get('password')
        user = User.objects.filter(id_card=id_card).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            employee = Employee.objects.filter(user=user).first()

            employee_data = {
                'id': user.id,
                'id_card': user.id_card,
                'type_id_card': employee.get_type_id_card_display(),
                'image': employee.image.url if employee.image else None,
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': employee.phone,
                'address': employee.address,
                'marital_status': employee.marital_status,
                'gender': employee.gender,
                'rh': employee.rh,
                'role': employee.role,
                'job': employee.job,
                'date_birth': employee.date_birth
            }

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data': employee_data
            }
        raise serializers.ValidationError('Credenciales inválidas')

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        token = data.get('refresh_token')
        if not token:
            raise serializers.ValidationError('Refresh token is required.')
        return data

    def save(self):
        try:
            token = RefreshToken(self.validated_data['refresh_token'])
            token.blacklist()  # Invalida el token de refresh
        except Exception as e:
            raise serializers.ValidationError(str(e))


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get('refresh')
        if not refresh_token:
            raise serializers.ValidationError('El token de actualización es requerido.')

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            return {
                'access': new_access_token,
                'refresh': str(refresh)  # O puedes retornar solo el nuevo token de acceso
            }

        except TokenError as e:
            raise serializers.ValidationError(f"Token inválido o expirado: {str(e)}")
