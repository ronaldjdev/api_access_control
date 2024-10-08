from django.core.management.base import BaseCommand
from employee.models import Employee

class Command(BaseCommand):
    help = 'Seed the database with test employees'

    def handle(self, *args, **kwargs):
        # Borra empleados previos de prueba si es necesario
        Employee.objects.all().delete()

        # Crear empleados de prueba
        empleados_prueba = [
            {'identification': '123456', 'name': 'Juan Pérez', 'email': 'juan@example.com', 'phone': '123456789', 'address': 'Calle Falsa 123', 'password': 'password123'},
            {'identification': '789101', 'name': 'María López', 'email': 'maria@example.com', 'phone': '987654321', 'address': 'Avenida Siempre Viva 742', 'password': 'password456'},
            {'identification': '112233', 'name': 'Carlos Gómez', 'email': 'carlos@example.com', 'phone': '555666777', 'address': 'Plaza Principal 1', 'password': 'password789'}
        ]

        # Insertar empleados en la base de datos
        for empleado_data in empleados_prueba:
            empleado = Employee(
                identification=empleado_data['identification'],
                name=empleado_data['name'],
                email=empleado_data['email'],
                phone=empleado_data['phone'],
                address=empleado_data['address']
            )
            empleado.set_password(empleado_data['password'])  # Encriptar la contraseña
            empleado.save()

        self.stdout.write(self.style.SUCCESS('Empleados de prueba creados correctamente.'))
