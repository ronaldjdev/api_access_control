from rest_framework import serializers
from ..models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'id_card': instance.user.id_card,
            'type_id_card': instance.get_type_id_card_display(),
            'name': instance.user.name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
            'phone': instance.phone,
            'address': instance.address,
            'marital_status': instance.get_marital_status_display(),
            'gender': instance.get_gender_display(),
            'rh': instance.rh,
            'role': instance.role,
            'job': instance.job,
            'image': instance.image.url if instance.image else None
        }