from django.contrib import admin
from .models import VehiculoEnVenta, ImagenVehiculo

class ImagenVehiculoInline(admin.TabularInline):
    model = ImagenVehiculo
    extra = 1

@admin.register(VehiculoEnVenta)
class VehiculoEnVentaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('vehiculo_oficial', 'usuario', 'color', 'kilometraje', 'numero_duenos', 'precio', 'negociable', 'acepta_permuta', 'descripcion')
        }),
    )
    inlines = [ImagenVehiculoInline]
    list_display = ('vehiculo_oficial', 'usuario', 'color', 'kilometraje', 'numero_duenos', 'precio', 'negociable', 'acepta_permuta', 'fecha_publicacion')
    search_fields = ('vehiculo_oficial__marca', 'vehiculo_oficial__modelo', 'usuario__username')
    list_filter = ('negociable', 'acepta_permuta', 'color')
    readonly_fields = ('vehiculo_oficial',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('usuario',)
        return self.readonly_fields
