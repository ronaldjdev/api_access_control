from django.db import models
from base.models import ModelBase
from user.models import User


# Create your models here.
class QrCode (ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Empleado',)
    qr_code = models.ImageField('Codigo QR', upload_to='qr/', blank=True, null=True)

    class Meta:
        verbose_name = 'Codigo QR'
        verbose_name_plural = 'Codigos QR'
        app_label = 'register_access'

class RegisterAccess(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Empleado',)
    type_access = models.CharField('Tipo de acceso',max_length=10, choices=[('IN', 'Ingreso'), ('OUT', 'Salida')])
    user_entry = models.DateTimeField('Ingreso',null=True, blank=True)
    user_exit = models.DateTimeField('Salida',null=True, blank=True)
    hours_worked = models.DecimalField('H. trabajadas', max_digits=5, decimal_places=2, default=0.00)
    extra_hours = models.DecimalField('H. extras', max_digits=5, decimal_places=2, default=0.00)
    qr_data = models.ForeignKey(QrCode, on_delete=models.CASCADE, verbose_name='Codigo QR',null=True, blank=True)

    class Meta:
        verbose_name = 'Registro de acceso'
        verbose_name_plural = 'Registros de acceso'
        app_label = 'register_access'

    def save(self, *args, **kwargs):
        # Calcular horas trabajadas y horas extras
        if self.user_entry and self.user_exit:
            # Calculamos la diferencia en horas
            work_duration = self.user_exit - self.user_entry
            hours = work_duration.total_seconds() / 3600  # Convertimos a horas

            # Jornada laboral estándar de 8 horas
            standard_work_hours = 8
            self.hours_worked = round(hours, 2)
            
            # Si trabajó más de 8 horas, calcular horas extras
            if hours > standard_work_hours:
                self.extra_hours = round(hours - standard_work_hours, 2)
            else:
                self.extra_hours = 0.00
        
        super().save(*args, **kwargs)