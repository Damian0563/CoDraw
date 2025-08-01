"""
ASGI config for codraw project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import codraw.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codraw.settings')
django_asgi_app=get_asgi_application()
application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            codraw.routing.websocket_urlpatterns
        )
    ),
})