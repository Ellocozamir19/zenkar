# Vistas (endpoints) para la API de usuarios
#
# Aquí se define cómo se registran, loguean, listan y eliminan usuarios desde el frontend o admin.
# Hay lógica especial para que solo los admins mayores puedan eliminar otros admins, y para evitar que alguien se borre a sí mismo.

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login
from .serializers import RegistroSerializer, LoginSerializer
from .models import Usuario
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse
import traceback
import logging
logger = logging.getLogger(__name__)

class RegistroView(APIView):
    # Permite registrar un usuario nuevo
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            print('=== INICIO REGISTRO ===')
            print('Datos recibidos en registro:', request.data)
            print('Content-Type:', request.content_type)
            print('Headers:', dict(request.headers))
            serializer = RegistroSerializer(data=request.data)
            print('Serializer creado, validando...')
            if serializer.is_valid():
                print('Serializer válido, guardando usuario...')
                user = serializer.save()
                print('Usuario registrado exitosamente:', user)
                return Response({
                    'mensaje': 'Usuario registrado correctamente',
                    'tipo_usuario': user.tipo_usuario
                }, status=status.HTTP_201_CREATED)
            else:
                print('Errores de validación del serializer:', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('=== ERROR EN REGISTRO ===')
            print('Tipo de error:', type(e).__name__)
            print('Mensaje de error:', str(e))
            print('Traceback completo:')
            traceback.print_exc()
            logger.error(f"Error en registro: {str(e)}", exc_info=True)
            from django.conf import settings
            return JsonResponse({
                'error': 'Error interno del servidor',
                'details': str(e) if settings.DEBUG else 'Error interno'
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    # Permite hacer login
    permission_classes = [AllowAny]
    def post(self, request):
        print('Datos recibidos en login:', request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            print('Usuario autenticado:', user)
            if user is not None:
                # Forzar backend si no está presente
                if not hasattr(user, 'backend'):
                    user.backend = settings.AUTHENTICATION_BACKENDS[0]
                login(request, user)
                user_data = RegistroSerializer(user).data
                print('Login exitoso, datos de usuario:', user_data)
                return Response(user_data)
            else:
                print('Usuario autenticado es None')
                return Response({'detail': 'Usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        print('Errores de autenticación:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioListView(generics.ListAPIView):
    # Devuelve la lista de todos los usuarios
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]

class UsuarioDeleteView(generics.DestroyAPIView):
    # Permite borrar usuarios, pero con reglas según el tipo de usuario
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user = request.user
        # Admin mayor puede eliminar admins, usuarios y vendedores, pero nunca a sí mismo ni a otro admin mayor
        if current_user.tipo_usuario == 'admin_mayor':
            if instance.tipo_usuario == 'admin_mayor':
                return Response({'detail': 'No puedes eliminar al admin mayor.'}, status=status.HTTP_403_FORBIDDEN)
            if instance.id == current_user.id:
                return Response({'detail': 'No puedes eliminarte a ti mismo.'}, status=status.HTTP_403_FORBIDDEN)
            return super().destroy(request, *args, **kwargs)
        # Admin normal solo puede eliminar usuarios y vendedores, no a sí mismo ni a otros admins
        if current_user.tipo_usuario == 'admin':
            if instance.tipo_usuario in ['admin', 'admin_mayor']:
                return Response({'detail': 'No puedes eliminar a otro admin o admin mayor.'}, status=status.HTTP_403_FORBIDDEN)
            if instance.id == current_user.id:
                return Response({'detail': 'No puedes eliminarte a ti mismo.'}, status=status.HTTP_403_FORBIDDEN)
            return super().destroy(request, *args, **kwargs)
        # Otros no pueden eliminar
        return Response({'detail': 'No tienes permisos para eliminar usuarios.'}, status=status.HTTP_403_FORBIDDEN)

class UsuarioMakeAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, id):
        user = Usuario.objects.get(id=id)
        # Solo el admin mayor puede hacer admin a otros
        if request.user.tipo_usuario != 'admin_mayor':
            return Response({'detail': 'Solo el admin mayor puede asignar admins.'}, status=status.HTTP_403_FORBIDDEN)
        user.tipo_usuario = 'admin'
        user.is_staff = True
        user.save()
        return Response({'mensaje': 'Usuario ahora es admin'})

class UsuarioEditView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def put(self, request, id):
        print('DEBUG Usuario autenticado:', request.user.username, 'tipo_usuario:', getattr(request.user, 'tipo_usuario', None), 'is_superuser:', getattr(request.user, 'is_superuser', None))
        try:
            user = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        # Un admin NO puede editar a otro admin ni al admin mayor
        if request.user.tipo_usuario == 'admin' and user.tipo_usuario in ['admin', 'admin_mayor']:
            return Response({'detail': 'No puedes editar a otro admin o admin mayor.'}, status=status.HTTP_403_FORBIDDEN)
        # Un admin mayor puede editar a cualquier usuario (excepto a sí mismo si es admin mayor)
        if request.user.tipo_usuario == 'admin_mayor' and user.id == request.user.id and user.tipo_usuario == 'admin_mayor':
            return Response({'detail': 'No puedes editarte a ti mismo como admin mayor.'}, status=status.HTTP_403_FORBIDDEN)
        # Validar username/email únicos
        if 'username' in data and Usuario.objects.exclude(id=id).filter(username=data['username']).exists():
            return Response({'detail': 'El nombre de usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'email' in data and Usuario.objects.exclude(id=id).filter(email=data['email']).exists():
            return Response({'detail': 'El correo ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'tipo_usuario' in data:
            # Solo el admin mayor puede cambiar el tipo de usuario a admin o admin mayor
            if data['tipo_usuario'] in ['admin', 'admin_mayor'] and request.user.tipo_usuario != 'admin_mayor':
                return Response({'detail': 'Solo el admin mayor puede asignar admins o admin mayor.'}, status=status.HTTP_403_FORBIDDEN)
            user.tipo_usuario = data['tipo_usuario']
            if data['tipo_usuario'] == 'admin':
                user.is_staff = True
            elif data['tipo_usuario'] != 'admin':
                user.is_staff = False
        # Permitir que el admin mayor cambie la contraseña de cualquier usuario
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        user.save()
        return Response({'mensaje': 'Usuario editado correctamente'})

class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

@method_decorator(csrf_exempt, name='dispatch')
class ConvertirVendedorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            user = Usuario.objects.get(id=id)
            # Solo el propio usuario o un admin puede convertir
            if request.user != user and not request.user.is_staff:
                return Response({'detail': 'No tienes permiso para convertir este usuario.'}, status=status.HTTP_403_FORBIDDEN)
            data = request.data.copy()
            data['tipo_usuario'] = Usuario.VENDEDOR
            serializer = RegistroSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensaje': 'Usuario convertido a vendedor correctamente.'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error al convertir a vendedor: {str(e)}", exc_info=True)
            return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=500)

@ensure_csrf_cookie
def csrf(request):
    # Devuelve el token CSRF en una cookie y en JSON
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE', '')})
