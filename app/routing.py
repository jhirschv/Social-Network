# network/routing.py
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat_room/', ChatConsumer.as_asgi()),
]