from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import models
from .models import Vehiculo
from collections import defaultdict

class VehiculoSugerenciasView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        q = request.GET.get('q', '').strip().lower()
        if not q:
            return Response([])
        # Agrupar por marca+modelo y contar versiones
        vehiculos = Vehiculo.objects.filter(
            models.Q(marca__icontains=q) | models.Q(modelo__icontains=q)
        ).values('marca', 'modelo', 'version', 'id')
        agrupados = defaultdict(list)
        for v in vehiculos:
            key = f"{v['marca']} {v['modelo']}".strip()
            agrupados[key].append(v)
        sugerencias = []
        for key, items in agrupados.items():
            versiones_set = set((v['version'] or '') for v in items)
            versiones = len(versiones_set)
            ids = [v['id'] for v in items]
            # Mostrar la versión aunque solo haya una
            modelos = items
            sugerencias.append({
                'label': f"{key} ({versiones} version{'es' if versiones != 1 else ''})",
                'ids': ids,
                'modelos': modelos
            })
        sugerencias = sorted(sugerencias, key=lambda x: -len(x['ids']))[:10]
        return Response(sugerencias)
