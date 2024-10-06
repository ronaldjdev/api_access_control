from django.db import models
from base.models import ModelBase


# Create your models here.

class Employee(ModelBase):
    identification = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        app_label = 'employee'
    