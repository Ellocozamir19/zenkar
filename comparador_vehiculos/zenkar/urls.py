"""
URL configuration for zenkar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def api_test(request):
    return JsonResponse({'message': 'API funcionando'})

def home(request):
    return HttpResponse('API Zenkar funcionando')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/vehiculos/', include('apps.vehiculos.urls')),
    path('api/ventas/', include('apps.ventas.urls')),
    path('api/resenas/', include('apps.reseñas.urls')),
    path('api/favoritos/', include('apps.favoritos.urls')),
    path('api/', api_test),
    path('', home),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
