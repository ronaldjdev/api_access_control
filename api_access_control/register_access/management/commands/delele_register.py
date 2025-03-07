from django.core.management.base import BaseCommand
from register_access.models import RegisterAccess

class Command(BaseCommand):
    help = 'Elimina todos los registros de acceso'

    def handle(self, *args, **kwargs):
        try:
            count, _ = RegisterAccess.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"{count} registros de acceso eliminados con éxito."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocurrió un error al eliminar los registros: {e}"))
