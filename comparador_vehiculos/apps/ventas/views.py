from django.shortcuts import render
from rest_framework import generics, permissions
from .models import VehiculoEnVenta
from .serializers import VehiculoEnVentaSerializer

class VehiculoEnVentaListCreateView(generics.ListCreateAPIView):
    queryset = VehiculoEnVenta.objects.all()
    serializer_class = VehiculoEnVentaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class VehiculoEnVentaDetailView(generics.RetrieveDestroyAPIView):
    queryset = VehiculoEnVenta.objects.all()
    serializer_class = VehiculoEnVentaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
