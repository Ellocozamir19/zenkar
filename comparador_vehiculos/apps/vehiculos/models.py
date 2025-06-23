# Modelo principal de autos para comparar
#
# Esta clase representa un auto/vehículo en la base de datos. Cada campo es una característica del auto.
# Por ejemplo: marca, modelo, año, motor, si tiene aire acondicionado, etc.
# Así puedes guardar y mostrar toda la info de los autos que se van a comparar en la app.
#
# Si algún campo no se sabe, se puede dejar vacío (null=True, blank=True).
from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    # Datos generales del auto
    marca = models.CharField(max_length=100, null=True, blank=True)  # Ej: Toyota
    modelo = models.CharField(max_length=100, null=True, blank=True) # Ej: Corolla
    anio = models.PositiveIntegerField(null=True, blank=True)        # Ej: 2020
    version = models.CharField(max_length=200, null=True, blank=True) # Ej: XLE
    categoria = models.CharField(max_length=100, null=True, blank=True) # Ej: SUV
    transmision = models.CharField(max_length=100, null=True, blank=True) # Manual/Automática
    combustible = models.CharField(max_length=100, null=True, blank=True) # Gasolina, Diesel, etc.
    motor = models.CharField(max_length=100, null=True, blank=True) # Ej: 1.8L
    puertas = models.PositiveSmallIntegerField(null=True, blank=True) # Número de puertas
    imagen = models.URLField(null=True, blank=True)  # URL de la imagen del auto
    imagen_archivo = models.ImageField(upload_to='vehiculos/', null=True, blank=True)  # Imagen subida desde el dispositivo

    # Motor y potencia
    cilindraje = models.CharField(max_length=100, null=True, blank=True) # Ej: 1800cc
    potencia_hp = models.CharField(max_length=100, null=True, blank=True) # Ej: 140hp
    torque = models.CharField(max_length=100, null=True, blank=True) # Ej: 180Nm
    alimentacion = models.CharField(max_length=100, null=True, blank=True) # Ej: Inyección
    arbol_levas = models.CharField(max_length=100, null=True, blank=True) # Tipo de árbol de levas
    valvulas = models.CharField(max_length=100, null=True, blank=True) # Número de válvulas

    # Dimensiones y rendimiento
    largo = models.CharField(max_length=100, null=True, blank=True) # Largo del auto
    ancho = models.CharField(max_length=100, null=True, blank=True) # Ancho
    alto = models.CharField(max_length=100, null=True, blank=True) # Alto
    peso = models.CharField(max_length=100, null=True, blank=True) # Peso
    volumen_baul = models.CharField(max_length=100, null=True, blank=True) # Capacidad del baúl
    traccion = models.CharField(max_length=100, null=True, blank=True) # Tracción (delantera, 4x4, etc.)
    capacidad_tanque = models.CharField(max_length=100, null=True, blank=True) # Capacidad de gasolina

    # Seguridad
    airbags = models.CharField(max_length=100, null=True, blank=True) # Número de airbags
    abs = models.BooleanField(null=True, blank=True) # ¿Tiene frenos ABS?
    frenos_delanteros = models.CharField(max_length=100, null=True, blank=True) # Tipo de frenos delanteros
    frenos_traseros = models.CharField(max_length=100, null=True, blank=True) # Tipo de frenos traseros
    bloqueo_central = models.BooleanField(null=True, blank=True) # ¿Tiene bloqueo central?
    cinturones = models.CharField(max_length=100, null=True, blank=True) # Tipo/cantidad de cinturones

    # Confort y extras
    aire_acondicionado = models.BooleanField(null=True, blank=True) # ¿Tiene aire?
    vidrios_electricos = models.BooleanField(null=True, blank=True) # ¿Tiene vidrios eléctricos?
    bluetooth = models.BooleanField(null=True, blank=True) # ¿Tiene bluetooth?
    usb = models.BooleanField(null=True, blank=True) # ¿Tiene USB?
    radio = models.BooleanField(null=True, blank=True) # ¿Tiene radio?

    # Dirección y suspensión
    direccion = models.CharField(max_length=100, null=True, blank=True) # Tipo de dirección
    suspension_delantera = models.CharField(max_length=100, null=True, blank=True) # Suspensión delantera
    suspension_trasera = models.CharField(max_length=100, null=True, blank=True) # Suspensión trasera

    def __str__(self):
        # Esto es lo que se muestra cuando imprimes un auto en la consola/admin
        return f"{self.marca} {self.modelo} {self.anio} {self.version}"
