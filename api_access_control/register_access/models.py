from django.db import models
from base.models import ModelBase
from employee.models import Employee

# Create your models here.

class RegisterAccess(ModelBase):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type_access = models.CharField(max_length=10, choices=[('IN', 'Ingreso'), ('OUT', 'Salida')])
    qr_data = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Registro de acceso'
        verbose_name_plural = 'Registros de acceso'
        app_label = 'register_access'
