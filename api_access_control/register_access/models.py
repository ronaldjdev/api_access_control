from django.db import models
from base.models import ModelBase
from user.models import User
from datetime import timedelta


# Create your models here.
class QrCode(ModelBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Empleado",
    )
    qr_code = models.ImageField("Codigo QR", upload_to="qr/", blank=True, null=True)

    class Meta:
        verbose_name = "Codigo QR"
        verbose_name_plural = "Codigos QR"
        app_label = "register_access"


class RegisterAccess(ModelBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Empleado",
    )
    type_access = models.CharField(
        "Tipo de acceso", max_length=10, choices=[("IN", "Ingreso"), ("OUT", "Salida")]
    )
    user_entry = models.DateTimeField("Ingreso", null=True, blank=True)
    user_exit = models.DateTimeField("Salida", null=True, blank=True)
    hours_worked = models.DecimalField(
        "H. trabajadas", max_digits=5, decimal_places=2, default=0.00
    )
    extra_hours = models.DecimalField(
        "H. ext diurnas", max_digits=5, decimal_places=2, default=0.00
    )
    extra_hours_night = models.DecimalField(
        "H. ext nocturnas", max_digits=5, decimal_places=2, default=0.00
    )
    remark = models.TextField("Observaciones", null=True, blank=True)
    qr_data = models.ForeignKey(
        QrCode,
        on_delete=models.CASCADE,
        verbose_name="Codigo QR",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Registro de acceso"
        verbose_name_plural = "Registros de acceso"
        app_label = "register_access"

    def save(self, *args, **kwargs):
        """
        Calcula las horas trabajadas, horas extras diurnas y horas extras nocturnas
        según los rangos establecidos y los descuentos aplicables según el cargo.
        """
        if self.user_entry and self.user_exit:
            # Duración total en horas entre entrada y salida
            work_duration = self.user_exit - self.user_entry
            total_hours = work_duration.total_seconds() / 3600  # Convertimos a horas

            # Jornada laboral estándar (8 horas)
            standard_work_hours = 8  # Jornada estándar de 8 horas

            # Descuento por cargo específico (si existe)
            if self.user.employee:
                if self.user.employee.job in [
                    "HOUSEKEEPING",
                    "GARDENER",
                    "MAINTENANCE",
                ]:
                    total_hours -= 1.5
                elif self.user.employee.job == "GOLF_PRO":
                    total_hours -= 2
                elif self.user.employee.job == "TENNIS_PRO":
                    total_hours -= 1

            # Calculamos las horas trabajadas totales
            self.hours_worked = round(total_hours, 2)

            # Calcular las horas extras diurnas (de 7 AM a 9 PM)
            day_extra_start = self.user_entry.replace(
                hour=7, minute=0, second=0, microsecond=0
            )  # 7:00 AM
            day_extra_end = self.user_entry.replace(
                hour=21, minute=0, second=0, microsecond=0
            )  # 9:00 PM

            # Asegurarse de que el cálculo se haga dentro del rango correcto
            if self.user_entry < day_extra_end:  # Si la entrada es antes de las 9:00 PM
                diurnal_extra_time = (min(self.user_exit, day_extra_end) - max(self.user_entry, day_extra_start)).total_seconds() / 3600
            else:
                diurnal_extra_time = 0

            # Calcular las horas extras nocturnas (de 9 PM a 7 AM)
            night_extra_start = self.user_entry.replace(
                hour=21, minute=0, second=0, microsecond=0
            )  # 9:00 PM
            night_extra_end = self.user_entry.replace(
                hour=7, minute=0, second=0, microsecond=0
            ) + timedelta(days=1)  # 7:00 AM del día siguiente

            # Asegurarse de que el cálculo se haga dentro del rango correcto
            if self.user_exit > night_extra_start:  # Si la salida es después de las 9:00 PM
                nocturnal_extra_time = (min(self.user_exit, night_extra_end) - max(self.user_entry, night_extra_start)).total_seconds() / 3600
            else:
                nocturnal_extra_time = 0

            # Asignar las horas extras diurnas y nocturnas
            self.extra_hours = round(max(diurnal_extra_time - standard_work_hours, 0), 2)
            self.extra_hours_night = round(nocturnal_extra_time, 2)

        # Llamamos al método save del modelo base
        super().save(*args, **kwargs)