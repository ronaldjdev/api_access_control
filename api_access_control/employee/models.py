from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

from base.models import ModelBase
from .choices import ID_CHOICES, GENDER, MARITAL_STATUS, RH


# Create your models here.
class UserManager(BaseUserManager):
    """Modelo Control de usuarios personalizados"""

    def _create_user(
        self,   id_card,
        username,   email,
        name, password, is_staff,
        is_superuser, **extra_fields
    ):
        user = self.model(
            id_card=id_card,
            username=username,
            email=email,
            name=name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self,   id_card,
        username,   email,
        name,  
        password=None, **extra_fields

    ):
        return self._create_user(
            id_card, username,
            email, name, password,
            False, False,
            **extra_fields
        )

    def create_superuser(
        self,   id_card,
        username,   email,
        name, password=None, **extra_fields

    ):
        return self._create_user(
            id_card, username,
            email, name, password,
            True, True,
            **extra_fields
        )

    
    def get_by_natural_key(self, email):
        return self.get(email=email)


class Employee(AbstractBaseUser, PermissionsMixin,ModelBase):
    id_card = models.CharField('Identificación', max_length=25, unique=True)
    type_id_card = models.CharField('Tipo de identificación',max_length=255, choices=ID_CHOICES, default=ID_CHOICES[0][0])
    username = models.CharField('Nombre de usuario',max_length=255, unique=True)
    name = models.CharField('Nombre',max_length=255)
    last_name = models.CharField('Apellido',max_length=255)
    email = models.EmailField('Email',max_length=255, unique=True)
    password = models.CharField('Contraseña',max_length=255)
    image = models.ImageField("Imagen Perfil", upload_to='profile/', blank=True)
    phone = models.CharField('Teléfono',max_length=255)
    address = models.CharField('Dirección',max_length=255)
    marital_status = models.CharField("Estado Civil", max_length=255, choices=MARITAL_STATUS, default=MARITAL_STATUS[0][0])
    gender = models.CharField('Genero',max_length=255, choices=GENDER, default=GENDER[0][0])
    rh = models.CharField('RH',max_length=255, choices=RH, default=RH[0][0])
    role = models.CharField('Rol',max_length=255, default='employee')
    job = models.CharField('Cargo',max_length=255, default='Servicio')

    is_staff = models.BooleanField("Staff", default=False)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "id_card", "type_id_card","email", "name",
        "last_name"
    ]
    
    objects = UserManager()
    
    def natural_key(self):
        return (self.email,)
    
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