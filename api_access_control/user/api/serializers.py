from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken

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
            'password',
        ]
        

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos de validated_data. Se utiliza el 
        método set_password para cifrar la contraseña. Luego, se guarda el 
        usuario en la base de datos.
        
        :param validated_data: diccionario con la información del usuario a 
        crear.
        :return: el usuario recién creado.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Usar el método set_password para cifrar
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Actualiza parcialmente un usuario. Solo se actualizan los campos que 
        estén presentes en validated_data. Si se actualiza alguno de los campos 
        esenciales (id_card, name, last_name, email), se valida su presencia.
        
        :param instance: el usuario a actualizar.
        :param validated_data: diccionario con los campos a actualizar.
        :return: el usuario actualizado.
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        # Si hay una nueva contraseña, se actualiza
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

    def validate(self, attrs):

        return attrs

class SignInSerializer(serializers.Serializer):
    id_card = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        id_card = data.get('id_card')
        password = data.get('password')
        user = User.objects.filter(id_card=id_card).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            employee = Employee.objects.filter(user=user.id).first()
            employee_data = {
                'id': user.id,
                'id_card': user.id_card,
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'employee': employee and {
                    'id': employee.id,
                    'type_id_card': employee.type_id_card,
                    'image': employee.image.url if employee.image else None,
                    'phone': employee.phone,
                    'address': employee.address,
                    'marital_status': employee.marital_status,
                    'gender': employee.gender,
                    'rh': employee.rh,
                    'job': employee.job,
                    'date_birth': employee.date_birth
                } or None,
            }

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data': employee_data
            }
        else:
            print("Error de autenticación")  # Para depuración
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

class RegisterSerializer(serializers.Serializer):
    id_card = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # Validación de que no exista otro usuario con la misma identificación
        id_card = data.get('id_card')
        if User.objects.filter(id_card=id_card).exists():
            raise serializers.ValidationError("Ya existe un usuario con esa identificación")

        # Valida el correo para que no se repita
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe un usuario con ese correo electrónico")

        # # Validación de que la contraseña tenga al menos 8 caracteres
        # password = data.get('password')
        # if len(password) < 8:
        #     raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres")

        # Validación de que la identificación sea un número
        id_card = data.get('id_card')
        if not id_card.isdigit():
            raise serializers.ValidationError("La identificación debe ser un número")
        
        # Valida el nombre de usuario para que no se repita
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario")

        return data


    def create(self, validated_data):
        # Creación del usuario
        user = User(
            id_card=validated_data['id_card'],
            username=validated_data['id_card'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])  # Cifrar la contraseña
        )
        user.save()
        return user
    
class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            # Intenta decodificar el token y verifica el usuario
            access_token = AccessToken(value)
            user_id = access_token['user_id']
            
            # Verifica si el usuario existe en la base de datos
            if not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError("Usuario no encontrado.")
                
        except Exception as e:
            raise serializers.ValidationError(f"Token inválido o expirado: {str(e)}")
        
        return value

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    recipient = serializers.EmailField()