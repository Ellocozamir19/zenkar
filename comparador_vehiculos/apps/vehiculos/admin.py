from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos generales', {
            'fields': ('marca', 'modelo', 'anio', 'version', 'categoria', 'transmision', 'combustible', 'motor', 'puertas')
        }),
        ('Motor', {
            'fields': ('cilindraje', 'potencia_hp', 'torque', 'alimentacion', 'arbol_levas', 'valvulas')
        }),
        ('Dimensiones y rendimiento', {
            'fields': ('largo', 'ancho', 'alto', 'peso', 'volumen_baul', 'traccion', 'capacidad_tanque')
        }),
        ('Seguridad', {
            'fields': ('airbags', 'abs', 'frenos_delanteros', 'frenos_traseros', 'bloqueo_central', 'cinturones')
        }),
        ('Confort', {
            'fields': ('aire_acondicionado', 'vidrios_electricos', 'bluetooth', 'usb', 'radio')
        }),
        ('Dirección y suspensión', {
            'fields': ('direccion', 'suspension_delantera', 'suspension_trasera')
        }),
    )
    list_display = ('marca', 'modelo', 'anio', 'version', 'categoria')
    search_fields = ('marca', 'modelo', 'version')
    list_filter = ('categoria', 'anio', 'marca')
