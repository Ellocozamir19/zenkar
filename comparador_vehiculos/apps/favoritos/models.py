# Modelo para guardar favoritos
#
# Esta clase representa un favorito guardado por un usuario. Puede ser cualquier objeto (vehículo, etc.)
# Guarda quién es el usuario, qué objeto es el favorito y cuándo lo guardó.
# Así cada usuario puede tener su propia lista de favoritos.
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Quién guardó el favorito
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Tipo de objeto (vehículo, etc.)
    object_id = models.PositiveIntegerField()  # ID del objeto favorito
    vehiculo = GenericForeignKey('content_type', 'object_id')  # Referencia al objeto real
    fecha_agregado = models.DateTimeField(auto_now_add=True)  # Cuándo se guardó

    class Meta:
        unique_together = ('usuario', 'content_type', 'object_id')  # No puedes guardar el mismo favorito dos veces

    def __str__(self):
        return f"Favorito de {self.usuario}: {self.vehiculo}"
