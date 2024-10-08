# Generated by Django 5.1.1 on 2024-10-08 04:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('register_access', '0002_alter_registeraccess_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeraccess',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='Empleado'),
        ),
        migrations.AlterField(
            model_name='registeraccess',
            name='qr_data',
            field=models.CharField(max_length=255),
        ),
    ]
