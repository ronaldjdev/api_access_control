from rest_framework import serializers
from ..models import QrCode, RegisterAccess

class RegisterAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterAccess
        fields = '__all__'
        read_only_fields = ['qr_code']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'employee_id': instance.employee.id,
            'employee_name': instance.employee.name if instance.employee else '',
            'type_access': instance.type_access,
            'employee_entry': instance.employee_entry,
            'employee_exit': instance.employee_exit,
            'hours_worked': instance.hours_worked,
            'extra_hours': instance.extra_hours,
            'qr_data': instance.qr_data
        }


class GenerateQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields ='__all__'
    
    def create(self, validated_data):
        return QrCode.objects.create(**validated_data)

