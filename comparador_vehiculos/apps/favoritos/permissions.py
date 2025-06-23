# Permiso personalizado para favoritos
#
# Esta clase sirve para que solo el dueño de un favorito pueda modificarlo o borrarlo.
# O sea, si guardaste un auto como favorito, solo tú puedes quitarlo o editarlo.
# Pero cualquiera puede ver los favoritos (lectura), aunque no sean suyos.
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Este método se ejecuta cuando alguien quiere hacer algo con un favorito específico.
    # Si es solo ver (GET, HEAD, OPTIONS), deja pasar.
    # Si es editar o borrar, solo deja si el usuario es el dueño.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario == request.user
