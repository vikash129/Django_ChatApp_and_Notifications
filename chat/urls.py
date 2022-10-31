# chat/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('chat/<str:room_name>/<str:user_name>', views.room_view, name='chat-room'),
]