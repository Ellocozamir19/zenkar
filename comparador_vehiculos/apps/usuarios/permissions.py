# Permiso personalizado para usuarios
#
# Esta clase sirve para que solo los admins puedan modificar usuarios (crear, editar, borrar).
# Los usuarios normales solo pueden ver la info, no modificarla.
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    # Si la petición es solo lectura (GET, HEAD, OPTIONS), deja pasar.
    # Si es algo más, solo deja si el usuario es admin.
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.tipo_usuario == 'admin'
