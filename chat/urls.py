from django.urls import path

from chat.views import MessagesView, RoomsView

urlpatterns = [
    path('chat/rooms/<room_id>/messages', MessagesView.as_view(), name='Room Messages'),
    path('chat/rooms', RoomsView.as_view(), name='Rooms'),
]
