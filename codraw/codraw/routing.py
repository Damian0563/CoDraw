from django.urls import re_path
import codraw.consumers

websocket_urlpatterns = [
    re_path(r'^ws/socket/(?P<room_name>[a-fA-F0-9\-]+)/?$',
            codraw.consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/(?P<room_name>[a-fA-F0-9\-]+)/?$',
            codraw.consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/.*$', codraw.consumers.ChatConsumer.as_asgi()),
]
