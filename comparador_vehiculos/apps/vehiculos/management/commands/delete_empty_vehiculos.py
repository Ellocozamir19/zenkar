from django.core.management.base import BaseCommand
from apps.vehiculos.models import Vehiculo

class Command(BaseCommand):
    help = 'Elimina vehículos que no tienen marca, modelo y año (vacíos)'

    def handle(self, *args, **options):
        vacios = Vehiculo.objects.filter(marca__isnull=True, modelo__isnull=True, anio__isnull=True)
        count = vacios.count()
        vacios.delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {count} vehículos vacíos.'))
