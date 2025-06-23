# Serializador de favoritos para la API
#
# Convierte los objetos Favorito en datos que se pueden enviar por la API (JSON),
# y también al revés: de JSON a objeto Favorito. Así el frontend puede mostrar y guardar favoritos fácil.

from rest_framework import serializers
from .models import Favorito

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = '__all__'
