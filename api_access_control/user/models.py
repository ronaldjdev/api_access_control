from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

from base.models import ModelBase


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

class User (AbstractBaseUser, PermissionsMixin, ModelBase):

    id_card = models.CharField('Identificación', max_length=25, unique=True)
    username = models.CharField('Nombre de usuario',max_length=255, unique=True)
    name = models.CharField('Nombre',max_length=255)
    last_name = models.CharField('Apellido',max_length=255)
    email = models.EmailField('Email',max_length=255, unique=True)
    password = models.CharField('Contraseña',max_length=255)

    is_active = models.BooleanField('Activo',default=True)
    is_staff = models.BooleanField('Administrador',default=False)
    is_superuser = models.BooleanField('Superusuario',default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name', 'id_card']

    objects = UserManager()

    def natural_key(self):
        return (self.email,)
    
    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        app_label = 'user'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)