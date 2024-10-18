from rest_framework import serializers
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
