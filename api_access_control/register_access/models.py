from django.db import models
from base.models import ModelBase
from user.models import User
from datetime import timedelta
from math import floor, ceil
import holidays

# Create your models here.


def custom_round(value):
    """
    Redondea el valor al entero siguiente si el decimal es mayor a 0.75,
    de lo contrario, al entero anterior.
    """
    decimal_part = floor(value) + 0.75
    if value > decimal_part:
        return ceil(value)
    else:
        return floor(value)


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
        Sobreescribe el método save para calcular las horas trabajadas y extras.
        Se consideran las siguientes reglas:
        - Si el usuario tiene un cargo de HOUSEKEEPING, GARDENER o MAINTENANCE, se descontan 1.5 horas.
        - Si el usuario tiene un cargo de GOLF_PRO, se descontan 2 horas.
        - Si el usuario tiene un cargo de TENNIS_PRO, se descontan 1 hora.
        - Se consideran 7 horas de trabajo estándar para días festivos y fines de semana.
        - Se consideran 8 horas de trabajo estándar para los demás días.
        - Las horas extras diurnas se calculan entre las 7 AM y las 9 PM.
        - Las horas extras nocturnas se calculan entre las 9 PM y las 7 AM.
        """
        if self.user_entry and self.user_exit:
            # Duración total en horas entre entrada y salida
            work_duration = self.user_exit - self.user_entry
            total_hours = work_duration.total_seconds() / 3600  # Convertimos a horas

            colombian_holidays = holidays.Colombia()
            is_holiday = self.user_entry.date() in colombian_holidays
            weekday = self.user_entry.weekday()

            # Jornada laboral estándar según el día de la semana
            if is_holiday or weekday == 6:
                standard_work_hours = 7
            elif weekday == 5:  # Sábado
                standard_work_hours = 4
            else:
                standard_work_hours = 8
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

            # Descuento por tiempo de almuerzo basado en el cargo

            # Calculamos las horas trabajadas totales
            self.hours_worked = custom_round(round(total_hours, 2))

            # Rangos para horas extras diurnas y nocturnas
            day_extra_start = self.user_entry.replace(
                hour=7, minute=0, second=0, microsecond=0
            )
            day_extra_end = self.user_entry.replace(
                hour=20, minute=59, second=59, microsecond=999999
            )
            night_extra_start = self.user_entry.replace(
                hour=21, minute=0, second=0, microsecond=0
            )
            night_extra_end = self.user_entry.replace(
                hour=6, minute=59, second=59, microsecond=999999
            ) + timedelta(days=1)

            # Calcular horas diurnas trabajadas (dentro del rango 7 AM - 9 PM)
            diurnal_worked = 0
            if self.user_exit > day_extra_start:
                diurnal_worked = (
                    min(self.user_exit, day_extra_end)
                    - max(self.user_entry, day_extra_start)
                ).total_seconds() / 3600

            # Calcular horas nocturnas trabajadas (dentro del rango 9 PM - 7 AM)
            nocturnal_worked = 0
            if self.user_exit > night_extra_start:
                nocturnal_worked = (
                    min(self.user_exit, night_extra_end)
                    - max(self.user_entry, night_extra_start)
                ).total_seconds() / 3600

            # Horas extras diurnas y nocturnas
            extra_diurnal = max(diurnal_worked - standard_work_hours, 0) 
            self.extra_hours = custom_round(round(extra_diurnal, 2))
            self.extra_hours_night = custom_round(round(nocturnal_worked, 2))

        # Guardar el registro
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     """
    #     Calcula las horas trabajadas, horas extras diurnas y horas extras nocturnas
    #     según los rangos establecidos y los descuentos aplicables según el cargo.
    #     """
    #     if self.user_entry and self.user_exit:
    #         # Duración total en horas entre entrada y salida
    #         work_duration = self.user_exit - self.user_entry
    #         total_hours = work_duration.total_seconds() / 3600  # Convertimos a horas

    #         # Jornada laboral estándar (8 horas)
    #         standard_work_hours = 8  # Jornada estándar de 8 horas

    #         # Descuento por cargo específico (si existe)
    #         if self.user.employee:
    #             if self.user.employee.job in [
    #                 "HOUSEKEEPING",
    #                 "GARDENER",
    #                 "MAINTENANCE",
    #             ]:
    #                 total_hours -= 1.5
    #             elif self.user.employee.job == "GOLF_PRO":
    #                 total_hours -= 2
    #             elif self.user.employee.job == "TENNIS_PRO":
    #                 total_hours -= 1

    #         # Calculamos las horas trabajadas totales
    #         self.hours_worked = custom_round(round(total_hours, 2))

    #         # Calcular las horas extras diurnas (de 7 AM a 9 PM)
    #         day_extra_start = self.user_entry.replace(
    #             hour=7, minute=0, second=0, microsecond=0
    #         )  # 7:00 AM
    #         day_extra_end = self.user_entry.replace(
    #             hour=20, minute=59, second=59, microsecond=999999
    #         )  # 9:00 PM

    #         # Asegurarse de que el cálculo se haga dentro del rango correcto
    #         if self.user_entry < day_extra_end:  # Si la entrada es antes de las 9:00 PM
    #             diurnal_extra_time = (
    #                 min(self.user_exit, day_extra_end)
    #                 - max(self.user_entry, day_extra_start)
    #             ).total_seconds() / 3600
    #         else:
    #             diurnal_extra_time = 0

    #         # Calcular las horas extras nocturnas (de 9 PM a 7 AM)
    #         night_extra_start = self.user_entry.replace(
    #             hour=21, minute=0, second=0, microsecond=0
    #         )  # 9:00 PM
    #         night_extra_end = self.user_entry.replace(
    #             hour=6, minute=59, second=59, microsecond=999999
    #         ) + timedelta(
    #             days=1
    #         )  # 7:00 AM del día siguiente

    #         # Asegurarse de que el cálculo se haga dentro del rango correcto
    #         if (
    #             self.user_exit > night_extra_start
    #         ):  # Si la salida es después de las 9:00 PM
    #             nocturnal_extra_time = (
    #                 min(self.user_exit, night_extra_end)
    #                 - max(self.user_entry, night_extra_start)
    #             ).total_seconds() / 3600
    #         else:
    #             nocturnal_extra_time = 0

    #         # Asignar las horas extras diurnas y nocturnas
    #         round_extra_hours = round(
    #             max(diurnal_extra_time - standard_work_hours, 0), 2
    #         )
    #         round_extra_hours_night = round((nocturnal_extra_time), 2)
    #         self.extra_hours = custom_round(round_extra_hours)
    #         self.extra_hours_night = custom_round(round_extra_hours_night)

    #     # Llamamos al método save del modelo base
    #     super().save(*args, **kwargs)
