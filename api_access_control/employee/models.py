from django.db import models
from user.models import User
from base.models import ModelBase
from .choices import ID_CHOICES, GENDER, MARITAL_STATUS, RH



class Employee(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_id_card = models.CharField('Tipo de identificación',max_length=255, choices=ID_CHOICES, default=ID_CHOICES[0][0])
    image = models.ImageField("Imagen Perfil", upload_to='profile/', blank=True)
    phone = models.CharField('Teléfono',max_length=255)
    address = models.CharField('Dirección',max_length=255)
    marital_status = models.CharField("Estado Civil", max_length=255, choices=MARITAL_STATUS, default=MARITAL_STATUS[0][0])
    gender = models.CharField('Genero',max_length=255, choices=GENDER, default=GENDER[0][0])
    rh = models.CharField('RH',max_length=255, choices=RH, default=RH[0][0])
    role = models.CharField('Rol',max_length=255, default='employee')
    job = models.CharField('Cargo',max_length=255, default='Servicio')

    
    def __str__(self):
        return f"{self.name} "
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        app_label = 'employee'

