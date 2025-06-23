# Serializador de autos para la API
#
# Esto convierte los objetos Vehiculo (de la base de datos) en datos que se pueden enviar por la API (JSON),
# y también al revés: de JSON a objeto Vehiculo. Así el frontend puede recibir y enviar info de autos fácil.

from rest_framework import serializers
from .models import Vehiculo

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo  # Le decimos qué modelo usar
        fields = '__all__'  # Incluye todos los campos del modelo (marca, modelo, etc.)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si hay imagen_archivo, devolver la URL absoluta
        request = self.context.get('request')
        if instance.imagen_archivo and hasattr(instance.imagen_archivo, 'url'):
            if request:
                data['imagen_archivo'] = request.build_absolute_uri(instance.imagen_archivo.url)
            else:
                data['imagen_archivo'] = instance.imagen_archivo.url
        else:
            data['imagen_archivo'] = None
        return data
