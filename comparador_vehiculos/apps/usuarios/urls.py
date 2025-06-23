from django.urls import path
from .views import RegistroView, LoginView, UsuarioListView, UsuarioDeleteView, UsuarioMakeAdminView, UsuarioEditView, UsuarioDetailView, ConvertirVendedorView, csrf

urlpatterns = [
    path('register/', RegistroView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('listar/', UsuarioListView.as_view(), name='usuario-listar'),
    path('<int:id>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-eliminar'),
    path('<int:id>/hacer_admin/', UsuarioMakeAdminView.as_view(), name='usuario-hacer-admin'),
    path('<int:id>/editar/', UsuarioEditView.as_view(), name='usuario-editar'),
    path('<int:id>/detalle/', UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('<int:id>/convertir_vendedor/', ConvertirVendedorView.as_view(), name='usuario-convertir-vendedor'),
    path('csrf/', csrf, name='csrf'),
]
