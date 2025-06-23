from django.urls import path
from .views import FavoritoListView, FavoritoCreateView, FavoritoDeleteView

urlpatterns = [
    path('listar/', FavoritoListView.as_view(), name='favorito-listar'),
    path('agregar/', FavoritoCreateView.as_view(), name='favorito-agregar'),
    path('eliminar/<int:pk>/', FavoritoDeleteView.as_view(), name='favorito-eliminar'),
]
