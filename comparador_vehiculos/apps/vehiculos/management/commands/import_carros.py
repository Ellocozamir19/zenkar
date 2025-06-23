import csv
from django.core.management.base import BaseCommand
from apps.vehiculos.models import Vehiculo
from django.conf import settings
import os

def clean(val):
    if val is None:
        return None
    val = str(val).strip().replace('"', '')
    if val == '' or val.lower() == 'nan':
        return None
    return val

def to_int(val):
    try:
        return int(float(val))
    except:
        return None

class Command(BaseCommand):
    help = 'Importa vehículos desde un archivo CSV (bdcarros.csv) al modelo Vehiculo.'

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'bdcarros.csv')
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f'No se encontró el archivo: {csv_path}'))
            return
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            raw_header = next(reader)
            header = [h.replace('"', '').replace("'", '').replace('\ufeff','').strip() for h in raw_header]
            print('DEBUG HEADER LIMPIO:', header)
            count = 0
            for i, row in enumerate(reader):
                if i == 0:
                    print('DEBUG ROW LIMPIO:', row)
                if len(row) != len(header):
                    continue
                data = dict(zip(header, row))
                vehiculo = Vehiculo(
                    marca=clean(data.get('brand')),
                    modelo=clean(data.get('model')),
                    anio=to_int(data.get('Year')),
                    version=clean(data.get('trim')),
                    categoria=clean(data.get('body_type')),
                    transmision=clean(data.get('transmission')),
                    combustible=clean(data.get('engine_type')),
                    motor=clean(data.get('engine_size')),
                    puertas=to_int(data.get('doors')),
                    imagen=clean(data.get('image')),
                    cilindraje=clean(data.get('engine_size')),
                    potencia_hp=clean(data.get('horsepower')),
                    torque=clean(data.get('torque')),
                    largo=clean(data.get('wheelbase')),
                    peso=clean(data.get('curb_weight')),
                    volumen_baul=clean(data.get('cargo_capacity')),
                    traccion=clean(data.get('drive_type')),
                )
                vehiculo.save()
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Se importaron {count} vehículos correctamente.'))
