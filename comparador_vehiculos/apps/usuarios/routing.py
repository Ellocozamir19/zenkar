from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/usuarios/(?P<user_id>\d+)/$', consumers.UsuarioConsumer.as_asgi()),
]
