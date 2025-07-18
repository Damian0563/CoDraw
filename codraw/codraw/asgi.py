"""
ASGI config for codraw project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import codraw.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codraw.settings')

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            codraw.routing.websocket_urlpatterns
        )
    ),
})