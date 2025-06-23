from django.urls import path
from .views import RegistroView, LoginView, UsuarioListView, UsuarioDeleteView, UsuarioMakeAdminView, UsuarioEditView, UsuarioDetailView, ConvertirVendedorView, csrf
from .views import (
    PeticionCambioPerfilView, PeticionCambioPerfilListView, PeticionCambioPerfilAprobarView, PeticionCambioPerfilRechazarView, MisPeticionesCambioPerfilView,
    UsuarioMeView,  # <-- Importar la vista
)

urlpatterns = [
    path('register/', RegistroView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('listar/', UsuarioListView.as_view(), name='usuario-listar'),
    path('<int:id>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-eliminar'),
    path('<int:id>/hacer_admin/', UsuarioMakeAdminView.as_view(), name='usuario-hacer-admin'),
    path('<int:id>/editar/', UsuarioEditView.as_view(), name='usuario-editar'),
    path('<int:id>/detalle/', UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('<int:id>/convertir_vendedor/', ConvertirVendedorView.as_view(), name='usuario-convertir-vendedor'),
    path('me/', UsuarioMeView.as_view(), name='usuario-me'),  # <-- Agregar la ruta
    path('csrf/', csrf, name='csrf'),
    path('peticion_cambio/', PeticionCambioPerfilView.as_view(), name='peticion-cambio-perfil'),
    path('peticiones_cambio/', PeticionCambioPerfilListView.as_view(), name='peticiones-cambio-listar'),
    path('peticion_cambio/<int:id>/aprobar/', PeticionCambioPerfilAprobarView.as_view(), name='peticion-cambio-aprobar'),
    path('peticion_cambio/<int:id>/rechazar/', PeticionCambioPerfilRechazarView.as_view(), name='peticion-cambio-rechazar'),
    path('mis_peticiones_cambio/', MisPeticionesCambioPerfilView.as_view(), name='mis-peticiones-cambio'),
]
