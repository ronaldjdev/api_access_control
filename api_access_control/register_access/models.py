from django.db import models
from api_access_control.base.models import ModelBase
from api_access_control.employee.models import Employee

# Create your models here.

class RegisterAccess(ModelBase):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type_access = models.CharField(max_length=10, choices=[('IN', 'Ingreso'), ('OUT', 'Salida')])
    qr_data = models.CharField(max_length=255)