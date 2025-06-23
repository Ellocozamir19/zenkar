from django.contrib import admin
from .models import Favorito

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vehiculo', 'fecha_agregado')
    search_fields = ('usuario__username',)
    list_filter = ('fecha_agregado',)
