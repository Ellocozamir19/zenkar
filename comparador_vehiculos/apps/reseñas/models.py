from django.db import models
from django.conf import settings
from apps.vehiculos.models import Vehiculo

class Resena(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    texto = models.TextField()
    puntuacion = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.vehiculo} por {self.usuario}"
