"""
ASGI config for bison project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from balance.consumer import BalanceConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bison.settings')

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/balance/', BalanceConsumer.as_asgi()),
    ]),
    "http": get_asgi_application(),
})
