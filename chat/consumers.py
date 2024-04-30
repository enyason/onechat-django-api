from enum import Enum

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import Message, Room
from users.models import User


class EventType(Enum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    MESSAGE = 'message'
    ERROR = 'error'


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None
        self.room_id = None

    async def emit_error_event(self, message):
        await self.send_json(
            {
                'event_type': EventType.ERROR.value,
                'message': message,
            }
        )
        await self.close()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        print("Connect...")
        print(f"room = {self.room_name}")
        print(f"room group = {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        await self.send_json(
            {
                "event_type": EventType.CONNECTED.value,
                'message': "Connected successfully!",
            }
        )

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        return await super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        event_type = content.get('event_type')
        message = content['data']['message']
        sender_id = content['data']['sender_id']

        try:

            author = User.objects.aget(id=sender_id)
            await Message.objects.acreate(
                author_id=sender_id,
                content=message,
                room_id=self.room_name
            )
            message_event_obj = {
                'event_type': EventType.MESSAGE.value,
                'message': 'New message received',
                'data': {
                    'message': message,
                    'sender': author.username
                }
            }

            print(f"new message = {message}")
            print(f"sender = {sender_id}")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'chat_message', 'message': message_event_obj}
            )

            # Get all users in this room group
            room = await Room.objects.aget(id=self.room_name)
            # participants_tokens = room.participants.values_list('fcm_token')
            print(room)
            # set up  fcmpy
            # create a data notification
            # send FMC notification to clients

        except  Exception as e:
            print(str(e))
            await self.emit_error_event(str(e))

        return await super().receive_json(content, **kwargs)

        # Receive message from room group

    async def chat_message(self, event):
        try:
            message = event["message"]
            await self.send_json(message)
        except Exception as e:
            print(str(e))
            pass
