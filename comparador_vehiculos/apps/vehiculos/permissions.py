# Permisos personalizados para la app de vehículos
#
# Esta clase sirve para controlar quién puede hacer qué en la API de autos.
# Básicamente, si eres admin puedes hacer de todo (crear, editar, borrar),
# pero si eres un usuario normal solo puedes ver la info, no modificarla.
#
# Esto es útil para que nadie venga a romper o borrar autos si no tiene permisos.
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    # Este método se ejecuta cada vez que alguien hace una petición a la API.
    # Si la petición es "segura" (GET, HEAD, OPTIONS), cualquiera puede ver los datos.
    # Si es algo más (POST, PUT, DELETE), solo deja pasar si el usuario está logueado y es staff (admin).
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
