from rest_framework import serializers
from ..models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de empleado.
    """
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        """
        Representación personalizada del modelo de empleado. Esto se utiliza cuando se generan datos, como en la API.
        
        :param instance: la instancia de empleado que se serializará.
        :return: un diccionario con la representación personalizada de la instancia de Empleado.
        """
        return {
            'id': instance.id,
            'id_card': instance.user.id_card,
            'type_id_card': instance.type_id_card,
            'user_id': instance.user.id,
            'username': instance.user.username,
            'name': instance.user.name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
            'phone': instance.phone,
            'address': instance.address,
            'marital_status': instance.marital_status,
            'gender': instance.gender,
            'rh': instance.rh,
            'job': instance.job,
            'image': instance.image.url if instance.image else None,
            'date_birth': instance.date_birth
        }