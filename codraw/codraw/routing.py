from django.urls import re_path
import codraw.consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', codraw.consumers.ChatConsumer.as_asgi()),
]