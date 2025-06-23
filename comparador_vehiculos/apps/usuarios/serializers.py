# Serializadores para usuarios (registro y login)
#
# Aquí se define cómo se crean usuarios nuevos y cómo se validan los datos de login.
# El registro solo permite crear admins si el que crea es superusuario.

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, PeticionCambioPerfil

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    def validate(self, data):
        if not data.get('acepta_politica'):
            raise serializers.ValidationError({'acepta_politica': 'Debes aceptar la política de privacidad.'})
        if not data.get('acepta_terminos'):
            raise serializers.ValidationError({'acepta_terminos': 'Debes aceptar los términos y condiciones.'})
        return data

    class Meta:
        model = Usuario
        fields = (
            'id', 'username', 'email', 'password', 'tipo_usuario',
            'tipo_documento', 'numero_documento', 'fecha_nacimiento', 'genero',
            'celular', 'telefono_fijo', 'direccion', 'ciudad', 'departamento', 'pais',
            'persona_natural', 'anios_experiencia', 'tipo_vehiculos', 'cantidad_vehiculos_mes',
            'licencia_vendedor', 'asociacion_sector', 'nombre_empresa', 'mostrar_redes', 'facebook', 'instagram', 'web',
            'recibir_novedades', 'mostrar_contacto', 'acepta_politica', 'acepta_terminos',
            'tiene_experiencia', 'tiene_licencia'
        )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        # Solo superusuarios pueden crear admin_mayor o admin
        tipo = validated_data.get('tipo_usuario', Usuario.USUARIO)
        request = self.context.get('request')
        if tipo in [Usuario.ADMIN, Usuario.ADMIN_MAYOR]:
            if not request or not request.user.is_superuser:
                validated_data['tipo_usuario'] = Usuario.USUARIO
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Credenciales incorrectas')

class PeticionCambioPerfilSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    admin_responde_username = serializers.CharField(source='admin_responde.username', read_only=True)

    class Meta:
        model = PeticionCambioPerfil
        fields = [
            'id', 'usuario', 'usuario_username', 'datos_nuevos', 'estado',
            'fecha_solicitud', 'fecha_respuesta', 'admin_responde', 'admin_responde_username', 'motivo_rechazo'
        ]
        read_only_fields = ['estado', 'fecha_solicitud', 'fecha_respuesta', 'admin_responde', 'admin_responde_username', 'usuario_username']
