import os
from django.db import models

from cloudinary.models import CloudinaryField

from user.models import User
from base.models import ModelBase
from .choices import ID_CHOICES, GENDER, MARITAL_STATUS, RH




def employee_image_upload_path(instance, filename):
    # Extraemos la extensión original del archivo
    ext = filename.split('.')[-1]
    # Definimos el nuevo nombre de archivo como el nombre del usuario con su identificación
    filename = f"{instance.user.name}_{instance.user.id_card}.{ext}"
    # Retornamos la ruta de guardado, por ejemplo en la carpeta 'profile/'
    return os.path.join('profile/', filename)

class Employee(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_id_card = models.CharField('Tipo de identificación', max_length=255, choices=ID_CHOICES, default=ID_CHOICES[0][0])
    # image = models.ImageField("Imagen Perfil", upload_to=employee_image_upload_path, blank=True)
    image = CloudinaryField('Imagen Perfil', blank=True)
    phone = models.CharField('Teléfono', max_length=255)
    address = models.CharField('Dirección', max_length=255)
    marital_status = models.CharField("Estado Civil", max_length=255, choices=MARITAL_STATUS, default=MARITAL_STATUS[0][0])
    gender = models.CharField('Genero', max_length=255, choices=GENDER, default=GENDER[0][0])
    rh = models.CharField('RH', max_length=255, choices=RH, default=RH[0][0])
    role = models.CharField('Rol', max_length=255, default='employee')
    job = models.CharField('Cargo', max_length=255, default='Servicio')
    date_birth = models.DateField('Fecha de nacimiento', null=True, blank=True)

    
    def __str__(self):
        return f"{self.user.name} {self.user.last_name}"
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        app_label = 'employee'

