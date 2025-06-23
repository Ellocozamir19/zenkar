# Modelo de usuario personalizado
#
# Esta clase representa a los usuarios de la app. Hereda de AbstractUser (el usuario estándar de Django)
# pero le agregamos el campo tipo_usuario para distinguir entre admin mayor, admin, vendedor y usuario normal.
# Así podemos dar permisos y mostrar paneles diferentes según el tipo de usuario.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ADMIN_MAYOR = 'admin_mayor'  # El jefe máximo
    ADMIN = 'admin'              # Admin normal
    VENDEDOR = 'vendedor'        # Vendedor
    USUARIO = 'usuario'          # Usuario común
    TIPO_USUARIO_CHOICES = [
        (ADMIN_MAYOR, 'Admin Mayor'),
        (ADMIN, 'Administrador'),
        (VENDEDOR, 'Vendedor'),
        (USUARIO, 'Usuario común'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default=USUARIO)

    # 🧾 Datos Personales
    tipo_documento = models.CharField(max_length=30, null=True, blank=True)
    numero_documento = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, null=True, blank=True)
    # 📱 Contacto
    celular = models.CharField(max_length=20, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    pais = models.CharField(max_length=100, null=True, blank=True)
    # 💼 Perfil Profesional
    persona_natural = models.CharField(max_length=10, null=True, blank=True)
    anios_experiencia = models.PositiveIntegerField(null=True, blank=True)
    tipo_vehiculos = models.CharField(max_length=100, null=True, blank=True)
    cantidad_vehiculos_mes = models.PositiveIntegerField(null=True, blank=True)
    licencia_vendedor = models.CharField(max_length=100, null=True, blank=True)
    asociacion_sector = models.CharField(max_length=100, null=True, blank=True)
    tiene_experiencia = models.BooleanField(null=True, blank=True)
    tiene_licencia = models.BooleanField(null=True, blank=True)
    # 🌐 Presencia Online
    mostrar_redes = models.BooleanField(default=False)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    web = models.URLField(null=True, blank=True)
    # ⚙️ Preferencias y Legal
    recibir_novedades = models.BooleanField(default=False)
    mostrar_contacto = models.BooleanField(default=True)
    acepta_politica = models.BooleanField(default=False)
    acepta_terminos = models.BooleanField(default=False)
    nombre_empresa = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # El primer superusuario creado será admin mayor automáticamente
        if not self.pk and Usuario.objects.filter(tipo_usuario=Usuario.ADMIN_MAYOR).count() == 0 and self.is_superuser:
            self.tipo_usuario = Usuario.ADMIN_MAYOR
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"

class PeticionCambioPerfil(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='peticiones_cambio')
    # Campos que el usuario quiere cambiar (guardados como JSON)
    datos_nuevos = models.JSONField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    admin_responde = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, related_name='peticiones_resueltas')
    motivo_rechazo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Petición de {self.usuario.username} ({self.estado})"
