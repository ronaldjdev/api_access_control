from django.db import models
from base.models import ModelBase
from user.models import User
from .utils.work_hours_utils import (
    calculate_total_hours,
    calculate_day_extra_hours,
    calculate_night_extra_hours,
    is_sunday_or_holiday,
    custom_round,
)
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
        "H. trabajadas", max_digits=5, decimal_places=2, blank=True, default=0
    )
    extra_hours = models.DecimalField(
        "H. ext diurnas", max_digits=5, decimal_places=2, blank=True, default=0
    )
    extra_hours_night = models.DecimalField(
        "H. ext nocturnas", max_digits=5, decimal_places=2, blank=True, default=0
    )
    remark = models.JSONField(default=dict, blank=True)
    qr_data = models.TextField("Datos QR", null=True, blank=True)

    class Meta:
        verbose_name = "Registro de acceso"
        verbose_name_plural = "Registros de acceso"
        app_label = "register_access"

    def calculate_hours(self):
        """Calcula las horas trabajadas y extras sin llamar a save() recursivamente."""
        if not self.user_entry or not self.user_exit:
            return

        job = getattr(self.user.employee, "job", None)

        # Determinar si es domingo o festivo
        is_holiday = is_sunday_or_holiday(self.user_entry)

        # Definir horas estándar según el día
        standard_work_hours = 8
        if is_holiday:
            if job in [
                "HOUSEKEEPING",
                "GARDENER",
                "MAINTENANCE",
                "MAINTENANCE_GOLF",
                "MAINTENANCE_POOL",
                "MAINTENANCE_TENNIS",
                "CHEF",
                "ASSISTANT_COOK",
            ]:
                standard_work_hours = 8
            else:
                standard_work_hours = 7
        elif self.user_entry.weekday() == 5:  # Sábado
            if job in [
                "HOUSEKEEPING",
                "GARDENER",
                "MAINTENANCE",
                "CHEF",
                "ASSISTANT_COOK",
            ]:
                standard_work_hours = 8
            else:
                standard_work_hours = 4

        # Calcular horas trabajadas
        total_hours = calculate_total_hours(self.user_entry, self.user_exit, job)
        self.hours_worked = custom_round(total_hours)

        # Calcular horas extras diurnas y nocturnas
        self.extra_hours = custom_round(
            calculate_day_extra_hours(
                self.user_entry, self.user_exit, standard_work_hours
            )
        )
        self.extra_hours_night = custom_round(
            calculate_night_extra_hours(self.user_entry, self.user_exit)
        )

    def save(self, *args, **kwargs):
        """Se asegura de calcular horas solo si hay entrada y salida, evitando bucles infinitos."""
        print("Guardando instancia de RegisterAccess")
        print(
            f"Valores actuales: user_entry={self.user_entry}, user_exit={self.user_exit}, type_access={self.type_access}"
        )

        if self.user_entry and self.user_exit:
            print("Ambos valores de entrada y salida están presentes")
            if self.type_access == "IN":
                print("Cambiando type_access de IN a OUT")
                self.type_access = "OUT"

            print("Calculando horas trabajadas")
            self.calculate_hours()

            print("Guardando con update_fields")
            super().save(
                update_fields=[
                    "hours_worked",
                    "extra_hours",
                    "extra_hours_night",
                    "type_access",
                    "user_exit",
                    "user_entry",
                ]
            )
        else:
            print("Faltan valores de entrada o salida, guardando normalmente")
            super().save(*args, **kwargs)

        print("Guardado completado")
