from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('chat-room/<str:room_uuid>/', consumers.ChatConsumer.as_asgi()),
    path('online-user/', consumers.OnlineUserConsumer.as_asgi()),
]