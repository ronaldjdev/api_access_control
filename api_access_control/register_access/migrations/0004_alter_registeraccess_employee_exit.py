# Generated by Django 5.1.1 on 2024-10-08 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_access', '0003_alter_registeraccess_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeraccess',
            name='employee_exit',
            field=models.DateTimeField(blank=True, verbose_name='Salida'),
        ),
    ]
