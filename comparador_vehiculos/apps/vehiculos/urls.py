from django.urls import path
from .views import (
    VehiculoListView, VehiculoDetailView, VehiculoCreateView, VehiculoDeleteView, VehiculoEditView,
    VehiculoPandasResumenView, VehiculoPandasResumenTemplateView, VehiculoUploadImagenView
)
from .sugerencias_api import VehiculoSugerenciasView

urlpatterns = [
    path('', VehiculoListView.as_view(), name='vehiculo-listar-root'),  # Permite /api/vehiculos/
    path('listar/', VehiculoListView.as_view(), name='vehiculo-listar'),
    path('detalle/<int:pk>/', VehiculoDetailView.as_view(), name='vehiculo-detalle'),
    path('crear/', VehiculoCreateView.as_view(), name='vehiculo-crear'),
    path('<int:id>/eliminar/', VehiculoDeleteView.as_view(), name='vehiculo-eliminar'),
    path('<int:id>/editar/', VehiculoEditView.as_view(), name='vehiculo-editar'),
    path('resumen-pandas/', VehiculoPandasResumenView.as_view(), name='vehiculo-resumen-pandas'), 
    path('resumen-pandas-html/', VehiculoPandasResumenTemplateView.as_view(), name='resumen_pandas_html'),
    path('upload_imagen/', VehiculoUploadImagenView.as_view(), name='vehiculo-upload-imagen'),
    path('sugerencias/', VehiculoSugerenciasView.as_view(), name='vehiculo-sugerencias'),
]
