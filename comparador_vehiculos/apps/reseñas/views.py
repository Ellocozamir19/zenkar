from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Resena
from .serializers import ResenaSerializer

class ResenaCreateView(generics.CreateAPIView):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ResenaListView(generics.ListAPIView):
    serializer_class = ResenaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        vehiculo_id = self.kwargs['vehiculo_id']
        return Resena.objects.filter(vehiculo_id=vehiculo_id)

class ResenaDeleteView(generics.DestroyAPIView):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticated]
