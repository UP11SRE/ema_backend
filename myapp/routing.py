   # file_manager/routing.py
from django.urls import path
from .consumers import FileProcessingConsumer

websocket_urlpatterns = [
       path('ws/file-processing/', FileProcessingConsumer.as_asgi()),
   ]