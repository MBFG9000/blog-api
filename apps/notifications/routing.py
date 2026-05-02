from django.urls import path

from apps.notifications.consumers import CommentsConsumer

websocket_urlpatterns = [
    path('ws/posts/<slug:slug>/comments/', CommentsConsumer.as_asgi()),
]