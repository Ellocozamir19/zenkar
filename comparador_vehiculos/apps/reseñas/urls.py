from django.urls import path
from .views import ResenaCreateView, ResenaListView, ResenaDeleteView

urlpatterns = [
    path('crear/', ResenaCreateView.as_view(), name='resena-crear'),
    path('listar/<int:vehiculo_id>/', ResenaListView.as_view(), name='resena-listar'),
    path('eliminar/<int:pk>/', ResenaDeleteView.as_view(), name='resena-eliminar'),
]
