from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from balance.consumer import BalanceConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/balance/', BalanceConsumer.as_asgi()),
    ])
})