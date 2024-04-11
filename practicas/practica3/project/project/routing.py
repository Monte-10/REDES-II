from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import MyConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": URLRouter([
        path("ws/path/", MyConsumer.as_asgi()),
    ]),
})