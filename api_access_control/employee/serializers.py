from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['identification', 'name', 'email', 'phone', 'address', 'password']

    # Sobrescribe para manejar la contraseña
    def create(self, validated_data):
        employee = Employee(**validated_data)
        employee.set_password(validated_data['password'])
        employee.save()
        return employee

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        
        # Si se pasa la contraseña, la encriptamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
