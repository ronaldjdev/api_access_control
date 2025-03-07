import os
from django.core.management.base import BaseCommand
from django.db import connection
import shutil

from register_access import views

class Command(BaseCommand):
    help = 'Elimina la tabla register_access_registeraccess y sus migraciones'

    def handle(self, *args, **kwargs):
        # Eliminar la tabla
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS register_access_registeraccess CASCADE;")
        self.stdout.write(self.style.SUCCESS('La tabla register_access_registeraccess ha sido eliminada.'))

        
        migrations_dir = os.path.join(views.BASE_DIR, 'register_access', 'migrations')
        self.stdout.write(f"Buscando migraciones en: {migrations_dir}")
        
        # Verificar si el directorio de migraciones existe
        if os.path.exists(migrations_dir):
            try:
                # Eliminar el directorio de migraciones y su contenido
                shutil.rmtree(migrations_dir)
                self.stdout.write(self.style.SUCCESS('El directorio de migraciones ha sido eliminado.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al eliminar el directorio de migraciones: {e}'))
                return
        else:
            self.stdout.write(self.style.WARNING('El directorio de migraciones no existe.'))
        
        # Volver a crear el directorio de migraciones y su archivo __init__.py
        try:
            os.makedirs(migrations_dir)
            with open(os.path.join(migrations_dir, '__init__.py'), 'w'):
                pass
            self.stdout.write(self.style.SUCCESS('El directorio de migraciones y __init__.py han sido recreados.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al recrear el directorio de migraciones: {e}'))
            return
        # Generar nuevas migraciones después de la eliminación
        # os.system("python manage.py makemigrations register_access")
        # self.stdout.write(self.style.SUCCESS('Migraciones actualizadas después de la eliminación de la tabla.'))
        
        # # Aplicar las migraciones pendientes
        # os.system("python manage.py migrate register_access")
        # self.stdout.write(self.style.SUCCESS('Migraciones aplicadas correctamente.'))
# /opt/render/project/src/api_access_control/