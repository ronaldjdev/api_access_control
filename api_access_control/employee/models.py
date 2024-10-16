from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from base.models import ModelBase
from .choices import ID_CHOICES, GENDER, MARITAL_STATUS


# Create your models here.

class Employee(ModelBase):
    id_card = models.CharField('Identificación',max_length=50, unique=True)
    type_id_card = models.CharField('Tipo de identificación',max_length=255, choices=ID_CHOICES, default=ID_CHOICES[0])
    name = models.CharField('Nombre',max_length=255)
    email = models.EmailField('Email',max_length=255, unique=True)
    password = models.CharField('Contraseña',max_length=255)
    image = models.ImageField("Imagen Perfil", upload_to='profile/', blank=True)
    phone = models.CharField('Teléfono',max_length=255)
    address = models.CharField('Dirección',max_length=255)
    marital_status = models.CharField("Estado Civil", max_length=255, choices=MARITAL_STATUS, default=MARITAL_STATUS[0])
    gender = models.CharField('Genero',max_length=255, choices=GENDER, default=GENDER[0])

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