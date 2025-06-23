# Vistas (endpoints) para la API de autos
#
# Aquí se definen las rutas y la lógica para mostrar, crear, editar y borrar autos desde el frontend o admin.
# Cada clase es una "vista" que responde a una URL específica de la API.
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vehiculo
from .serializers import VehiculoSerializer
import pandas as pd  # <--- Integración de Pandas
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

# Create your views here.

class VehiculoListView(generics.ListAPIView):
    # Devuelve la lista de todos los autos
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoDetailView(generics.RetrieveAPIView):
    # Devuelve el detalle de un auto específico
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoCreateView(generics.CreateAPIView):
    # Permite crear un auto nuevo (solo admins)
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAdminUser]

class VehiculoDeleteView(generics.DestroyAPIView):
    # Permite borrar un auto (solo admins)
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

class VehiculoEditView(APIView):
    # Permite editar un auto (solo admins)
    permission_classes = [permissions.IsAdminUser]
    def put(self, request, id):
        try:
            vehiculo = Vehiculo.objects.get(id=id)
        except Vehiculo.DoesNotExist:
            return Response({'detail': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehiculoSerializer(vehiculo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Vehículo editado correctamente'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehiculoPandasResumenView(APIView):
    """
    Vista que usa Pandas para mostrar un resumen de autos por marca y modelo.
    Devuelve un JSON con el conteo de autos agrupados por marca y modelo recuerde eso profe -_-
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        # Tomamos todos los autos de la base
        queryset = Vehiculo.objects.all().values('marca', 'modelo')
        df = pd.DataFrame(list(queryset))
        if df.empty:
            return Response({'resumen': [], 'mensaje': 'No hay autos cargados.'})
        resumen = (
            df.groupby(['marca', 'modelo'])
              .size()
              .reset_index(name='cantidad')
              .sort_values(['marca', 'cantidad'], ascending=[True, False])
        )
        return Response({'resumen': resumen.to_dict(orient='records')})

class VehiculoPandasResumenTemplateView(TemplateView):
    template_name = 'vehiculos/resumen_pandas.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        import pandas as pd
        from .models import Vehiculo
        queryset = Vehiculo.objects.all().values('marca', 'modelo')
        df = pd.DataFrame(list(queryset))
        if df.empty:
            resumen = []
        else:
            resumen = (
                df.groupby(['marca', 'modelo'])
                  .size()
                  .reset_index(name='cantidad')
                  .sort_values(['marca', 'cantidad'], ascending=[True, False])
                  .to_dict(orient='records')
            )
        return render(request, self.template_name, {'resumen': resumen})

class VehiculoUploadImagenView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        imagen = request.FILES.get('imagen')
        if not imagen:
            return Response({'error': 'No se envió ninguna imagen'}, status=status.HTTP_400_BAD_REQUEST)
        from django.core.files.storage import default_storage
        path = default_storage.save(f"vehiculos/{imagen.name}", imagen)
        url = request.build_absolute_uri(settings.MEDIA_URL + path.split('media/')[-1])
        return Response({'url': url, 'imagen': path}, status=status.HTTP_201_CREATED)
