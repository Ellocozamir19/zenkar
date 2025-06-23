from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('tipo_usuario',)

# Register your models here.
