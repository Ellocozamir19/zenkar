import json
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
    help = 'Importa vehículos desde un archivo JSON (bdcarros.json) al modelo Vehiculo.'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'bdcarros.json')
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'No se encontró el archivo: {json_path}'))
            return
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                self.stdout.write('JSON vacío')
                return
            # Extraer header y preparar campos
            first = list(data[0].keys())[0]
            header = [h.replace('"', '').replace("'", '').replace('\ufeff','').strip() for h in first.split(',')]
            print('DEBUG HEADER FINAL:', header)
            count = 0
            for i, item in enumerate(data):
                values = list(item.values())[0].split(',')
                if i == 0:
                    print('DEBUG VALUES:', values)
                if len(values) != len(header):
                    continue
                row = dict(zip(header, values))
                vehiculo = Vehiculo(
                    marca=clean(row.get('brand')),
                    modelo=clean(row.get('model')),
                    anio=to_int(row.get('Year')),
                    version=clean(row.get('trim')),
                    categoria=clean(row.get('body_type')),
                    transmision=clean(row.get('transmission')),
                    combustible=clean(row.get('engine_type')),
                    motor=clean(row.get('engine_size')),
                    puertas=to_int(row.get('doors')),
                    imagen=clean(row.get('image')),
                    cilindraje=clean(row.get('engine_size')),
                    potencia_hp=clean(row.get('horsepower')),
                    torque=clean(row.get('torque')),
                    largo=clean(row.get('wheelbase')),
                    peso=clean(row.get('curb_weight')),
                    volumen_baul=clean(row.get('cargo_capacity')),
                    traccion=clean(row.get('drive_type')),
                )
                vehiculo.save()
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Se importaron {count} vehículos correctamente.'))
