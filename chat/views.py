from rest_framework import status
from rest_framework.views import APIView

from chat.models import Message
from chat.serializers import MessageSerializer
from common.http_response_messages import success_messages
from common.http_response_utils import http_success_response


class MessagesView(APIView):

    def get(self, request, room_id):
        messages_qs = Message.objects.filter(room_id=room_id)
        messages_serializer = MessageSerializer(messages_qs, many=True)

        return http_success_response(message=success_messages['room_messages_retrieved'],
                                     data={
                                         'messages': messages_serializer.data,
                                         'response_code': 'room_messages_retrieved'
                                     },
                                     http_status=status.HTTP_201_CREATED)
