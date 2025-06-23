from django.db import models
from django.conf import settings
from apps.vehiculos.models import Vehiculo

class VehiculoEnVenta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehiculo_oficial = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    color = models.CharField(max_length=30, null=True, blank=True)
    kilometraje = models.PositiveIntegerField(null=True, blank=True)
    numero_duenos = models.PositiveSmallIntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    negociable = models.BooleanField(default=False)
    acepta_permuta = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehiculo_oficial} en venta por {self.usuario}"

class ImagenVehiculo(models.Model):
    vehiculo_venta = models.ForeignKey(VehiculoEnVenta, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='vehiculos_en_venta/')

    def __str__(self):
        return f"Imagen de {self.vehiculo_venta}"
