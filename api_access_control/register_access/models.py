from django.db import models
from base.models import ModelBase
from employee.models import Employee

# Create your models here.

class RegisterAccess(ModelBase):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado',)
    type_access = models.CharField('Tipo de acceso',max_length=10, choices=[('IN', 'Ingreso'), ('OUT', 'Salida')])
    employee_entry = models.DateTimeField('Ingreso',auto_now_add=True, blank=True)
    employee_exit = models.DateTimeField('Salida',auto_now=True)
    qr_data = models.CharField('Qr',max_length=255)

    class Meta:
        verbose_name = 'Registro de acceso'
        verbose_name_plural = 'Registros de acceso'
        app_label = 'register_access'
