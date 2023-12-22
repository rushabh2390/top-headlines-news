"""
ASGI config for newsapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
# import django

# django.setup()

from django.core.asgi import get_asgi_application
asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from news.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapi.settings')


application = ProtocolTypeRouter({
    "http": asgi_application,  # Regular HTTP handling by Django
    "websocket": URLRouter(websocket_urlpatterns),  # WebSocket handling
})