from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'id_card', 
            'type_id_card',
            'name', 
            'email', 
            'image',
            'phone', 
            'address', 
            'marital_status',
            'gender'
            ]

    # Sobrescribe para manejar la contraseña
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        
        # Si se pasa la contraseña, la encriptamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
