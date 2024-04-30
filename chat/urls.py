from django.urls import path

from chat.views import MessagesView

urlpatterns = [
    path('chat/<room_id>/messages', MessagesView.as_view(), name='Room Messages'),
]
