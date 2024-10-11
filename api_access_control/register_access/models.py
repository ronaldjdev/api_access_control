from django.db import models
from base.models import ModelBase
from employee.models import Employee


# Create your models here.

class RegisterAccess(ModelBase):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado',)
    type_access = models.CharField('Tipo de acceso',max_length=10, choices=[('IN', 'Ingreso'), ('OUT', 'Salida')])
    employee_entry = models.DateTimeField('Ingreso',null=True, blank=True)
    employee_exit = models.DateTimeField('Salida',null=True, blank=True)
    hours_worked = models.DecimalField('Horas trabajadas', max_digits=5, decimal_places=2, default=0.00)
    extra_hours = models.DecimalField('Horas extras', max_digits=5, decimal_places=2, default=0.00)
    qr_data = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Registro de acceso'
        verbose_name_plural = 'Registros de acceso'
        app_label = 'register_access'

    def save(self, *args, **kwargs):
        # Calcular horas trabajadas y horas extras
        if self.employee_entry and self.employee_exit:
            # Calculamos la diferencia en horas
            work_duration = self.employee_exit - self.employee_entry
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