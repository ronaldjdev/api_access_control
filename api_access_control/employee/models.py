import os
from django.db import models
from cloudinary.models import CloudinaryField
from user.models import User
from base.models import ModelBase
from base.choices import ID_CHOICES, GENDER, MARITAL_STATUS, RH, JOBS


def employee_image_upload_path(instance, filename):
    """Genera una ruta dinámica para la imagen de perfil del empleado."""
    ext = filename.split(".")[-1]
    if instance.user:
        filename = f"{instance.user.name or 'Empleado'}_{instance.user.id_card or '000000'}.{ext}"
    else:
        filename = f"empleado_desconocido.{ext}"
    return os.path.join("profile/", filename)


class Employee(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Empleado", null=True, blank=True)
    type_id_card = models.CharField(
        "Tipo de identificación",
        max_length=255,
        choices=ID_CHOICES,
        default=ID_CHOICES[0][0],
    )
    image = CloudinaryField("Imagen Perfil", blank=True)
    phone = models.CharField("Teléfono", max_length=255)
    address = models.CharField("Dirección", max_length=255)
    marital_status = models.CharField(
        "Estado Civil",
        max_length=255,
        choices=MARITAL_STATUS,
        default=MARITAL_STATUS[0][0],
    )
    gender = models.CharField(
        "Género", max_length=255, choices=GENDER, default=GENDER[0][0]
    )
    rh = models.CharField("Rh", max_length=255, choices=RH, default=RH[0][0])
    job = models.CharField("Cargo", max_length=255, choices=JOBS, default=JOBS[0][0])
    date_birth = models.DateField("Fecha de nacimiento", null=True, blank=True)

    def __str__(self):
        """Devuelve una representación en cadena del empleado."""
        if self.user:
            return f"{self.user.name or 'Sin nombre'} {self.user.last_name or 'Sin apellido'}"
        return "Empleado sin usuario asociado"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        app_label = "employee"
