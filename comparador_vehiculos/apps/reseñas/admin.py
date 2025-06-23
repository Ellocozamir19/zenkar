from django.contrib import admin
from .models import Resena

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'usuario', 'puntuacion', 'fecha')
    search_fields = ('vehiculo__marca', 'usuario__username')
    list_filter = ('puntuacion', 'vehiculo')
