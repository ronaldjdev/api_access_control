# Generated by Django 5.1.1 on 2024-10-08 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_access', '0007_alter_registeraccess_employee_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeraccess',
            name='employee_entry',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ingreso'),
        ),
    ]
