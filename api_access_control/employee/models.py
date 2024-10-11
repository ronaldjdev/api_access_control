from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from base.models import ModelBase


# Create your models here.

class Employee(ModelBase):
    identification = models.CharField('Identificación',max_length=50, unique=True)
    name = models.CharField('Nombre',max_length=255)
    email = models.EmailField('Email',max_length=255, unique=True)
    phone = models.CharField('Teléfono',max_length=255)
    address = models.CharField('Dirección',max_length=255)
    password = models.CharField('Contraseña',max_length=255)

    def __str__(self):
        return f"{self.name} "
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        app_label = 'employee'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)