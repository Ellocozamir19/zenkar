from django.urls import path
from .views import VehiculoEnVentaListCreateView, VehiculoEnVentaDetailView

urlpatterns = [
    path('listar/', VehiculoEnVentaListCreateView.as_view(), name='venta-listar'),
    path('detalle/<int:pk>/', VehiculoEnVentaDetailView.as_view(), name='venta-detalle'),
    path('eliminar/<int:pk>/', VehiculoEnVentaDetailView.as_view(), name='venta-eliminar'),
]
