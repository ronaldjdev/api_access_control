import pytz
from rest_framework import serializers
from ..models import QrCode, RegisterAccess


class RegisterAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterAccess
        fields = '__all__'
        read_only_fields = ['qr_code']

    def to_representation(self, instance):
        # Zona horaria de Bogotá
        tz = pytz.timezone('America/Bogota')

        # Convertir las fechas a la zona horaria de Bogotá
        user_entry = instance.user_entry.astimezone(tz) if instance.user_entry else None
        user_exit = instance.user_exit.astimezone(tz) if instance.user_exit else None

        # Convertir las fechas al formato "YYYY-MM-DDTHH:MM:SS"
        user_entry_str = user_entry.strftime('%Y-%m-%dT%H:%M:%S') if user_entry else ''
        user_exit_str = user_exit.strftime('%Y-%m-%dT%H:%M:%S') if user_exit else ''

        return {
            'id': instance.id,
            'user_id': instance.user.id,
            'user_name': instance.user.name if instance.user else '',
            'type_access': instance.type_access,
            'user_entry': user_entry_str,
            'user_exit': user_exit_str,
            'hours_worked': instance.hours_worked,
            'extra_hours': instance.extra_hours,
            'extra_hours_night': instance.extra_hours_night,
            'qr_data': instance.qr_data
        }


class GenerateQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields ='__all__'
    
    def create(self, validated_data):
        return QrCode.objects.create(**validated_data)

