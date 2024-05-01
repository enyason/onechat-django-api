from rest_framework import status
from rest_framework.views import APIView

from chat.models import Message, Room
from chat.serializers import MessageSerializer, RoomSerializer
from common.http_response_messages import success_messages
from common.http_response_utils import http_success_response


class MessagesView(APIView):

    def get(self, request, room_id):
        messages_qs = Message.objects.filter(room_id=room_id)
        messages_serializer = MessageSerializer(messages_qs, many=True)

        return http_success_response(message=success_messages['room_messages_retrieved'],
                                     code='room_messages_retrieved',
                                     data=messages_serializer.data,
                                     http_status=status.HTTP_200_OK)


class RoomsView(APIView):

    def get(self, request):
        messages_qs = Room.objects.all()
        messages_serializer = RoomSerializer(messages_qs, many=True)

        return http_success_response(message=success_messages['rooms_retrieved'],
                                     code='rooms_retrieved',
                                     data=messages_serializer.data,
                                     http_status=status.HTTP_200_OK)
