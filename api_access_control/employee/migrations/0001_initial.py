# Generated by Django 5.1.1 on 2025-03-28 07:32

import cloudinary.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_id_card', models.CharField(choices=[('NN', 'No proporciona'), ('RC', 'Registro civil'), ('TI', 'Tarjeta de identidad'), ('CC', 'Cedula de ciudadania'), ('TE', 'Tarjeta de extranjeria'), ('CE', 'Cedula de extranjeria'), ('NIT', 'N° Identificacion tributaria'), ('PS', 'Pasaporte'), ('TPE', 'Tipo de documento extranjero')], default='NN', max_length=255, verbose_name='Tipo de identificación')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='Imagen Perfil')),
                ('phone', models.CharField(max_length=255, verbose_name='Teléfono')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('marital_status', models.CharField(choices=[('NN', 'No registra'), ('S', 'Soltero'), ('C', 'Casado'), ('UL', 'Union Libre')], default='NN', max_length=255, verbose_name='Estado Civil')),
                ('gender', models.CharField(choices=[('NN', 'No registra'), ('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otros')], default='NN', max_length=255, verbose_name='Genero')),
                ('rh', models.CharField(choices=[('NN', 'No registra'), ('O+', 'O Positivo'), ('O-', 'O Negativo'), ('A+', 'A Positivo'), ('A-', 'A Negativo'), ('B+', 'B Positivo'), ('B-', 'B Negativo'), ('AB+', 'AB Positivo'), ('AB-', 'AB Negativo')], default='NN', max_length=255, verbose_name='Rh')),
                ('job', models.CharField(choices=[('NN', 'No registra'), ('ADMIN', 'Administrador'), ('SUBDIRECTOR', 'Subdirector'), ('RECEPTION', 'Recepcionista'), ('TREASURY', 'Tesorería'), ('IT_MANAGER', 'Coordinador de Sistemas'), ('MAINTENANCE', 'Mantenimiento General'), ('MAINTENANCE_TENNIS', 'Mantenimiento de Tenis'), ('MAINTENANCE_GOLF', 'Mantenimiento de Golf'), ('MAINTENANCE_POOL', 'Mantenimiento de Piscina'), ('GOLF_PRO', 'Profesional de Golf'), ('TENNIS_PRO', 'Profesional de Tenis'), ('LIFEGUARD', 'Salvavidas'), ('CHEF', 'Chef'), ('WAITER', 'Mesero'), ('HOUSEKEEPING', 'Servicio de Limpieza'), ('EVENT_MANAGER', 'Gerente de Eventos'), ('SECURITY', 'Seguridad'), ('GARDENER', 'Jardinero'), ('ACCOUNTANT', 'Contador'), ('HR', 'Recursos Humanos'), ('MEMBER_RELATIONS', 'Relaciones con Miembros'), ('COOK', 'Cocinero'), ('HEAD_CHEF', 'Jefe de Cocina'), ('SERVICE_ADMIN', 'Administración de Servicios')], default='NN', max_length=255, verbose_name='Cargo')),
                ('date_birth', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
    ]
