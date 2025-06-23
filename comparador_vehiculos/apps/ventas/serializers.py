from rest_framework import serializers
from .models import VehiculoEnVenta, ImagenVehiculo

class ImagenVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenVehiculo
        fields = ['id', 'imagen']

class VehiculoEnVentaSerializer(serializers.ModelSerializer):
    imagenes = ImagenVehiculoSerializer(many=True, read_only=True)
    class Meta:
        model = VehiculoEnVenta
        fields = '__all__'
