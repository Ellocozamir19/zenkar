# Vistas (endpoints) para la API de favoritos
#
# Aquí se define cómo se muestran, crean y borran los favoritos de cada usuario.
# Solo puedes ver y modificar tus propios favoritos (no los de otros).

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Favorito
from .serializers import FavoritoSerializer

class FavoritoListView(generics.ListAPIView):
    # Devuelve la lista de favoritos del usuario logueado
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)

class FavoritoCreateView(generics.CreateAPIView):
    # Permite guardar un nuevo favorito (solo si estás logueado)
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class FavoritoDeleteView(generics.DestroyAPIView):
    # Permite borrar un favorito (solo si es tuyo)
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)
