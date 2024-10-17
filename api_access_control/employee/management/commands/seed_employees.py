from django.core.management.base import BaseCommand
from employee.models import Employee

class Command(BaseCommand):
    help = 'Seed the database with test employees and a superuser'

    def handle(self, *args, **kwargs):
        # Borra empleados previos de prueba si es necesario
        Employee.objects.all().delete()

        # Crear empleados de prueba
        empleados_prueba = [
            {'id_card': '123456', 'username': 'juanp', 'email': 'juan@example.com', 'name': 'Juan', 'last_name': 'Pérez', 'password': 'password123', 'phone': '123456789', 'address': 'Calle Falsa 123'},
            {'id_card': '789101', 'username': 'marial', 'email': 'maria@example.com', 'name': 'María', 'last_name': 'López', 'password': 'password456', 'phone': '987654321', 'address': 'Avenida Siempre Viva 742'},
            {'id_card': '112233', 'username': 'carlosg', 'email': 'carlos@example.com', 'name': 'Carlos', 'last_name': 'Gómez', 'password': 'password789', 'phone': '555666777', 'address': 'Plaza Principal 1'}
        ]

        for empleado_data in empleados_prueba:
            Employee.objects.create_user(
                id_card=empleado_data['id_card'],
                username=empleado_data['username'],
                email=empleado_data['email'],
                name=empleado_data['name'],
                last_name=empleado_data['last_name'],
                password=empleado_data['password'],
                phone=empleado_data['phone'],
                address=empleado_data['address']
            )

        # Crear superusuario para pruebas
        if not Employee.objects.filter(username='admin').exists():
            Employee.objects.create_superuser(
                id_card='111111',  # Cambia a un número entero
                username='admin',
                email='admin@example.com',
                name='Admin',
                last_name='User',
                password='1111'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario de prueba creado correctamente.'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe.'))

        self.stdout.write(self.style.SUCCESS('Empleados de prueba creados correctamente.'))
