import os
from enum import Enum

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from pyfcm import FCMNotification

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
        self.user = None
        self.room_group_name = None
        self.room_name = None

    async def emit_error_event(self, message):
        await self.send_json(
            {
                'event_type': EventType.ERROR.value,
                'message': message,
            }
        )
        await self.close()

    async def connect(self):
        user = self.scope["user"]

        await self.accept()

        print(f"This is a user = {user}")
        if isinstance(user, AnonymousUser):
            await self.emit_error_event("Access not granted")

        print(f"user = {user}")
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        print("Connect...")
        print(f"room = {self.room_name}")
        print(f"room group = {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

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
        sender = content['data']['sender']

        try:

            author = await User.objects.aget(username=sender)
            message_obj = await Message.objects.acreate(
                author=author,
                content=message,
                room_id=self.room_name
            )
            message_event_obj = {
                'event_type': EventType.MESSAGE.value,
                'message': 'New message received',
                'data': {
                    'message_id': str(message_obj.id),
                    'message': message,
                    'sender': author.username
                }
            }

            print(f"new message = {message}")
            print(f"sender = {sender}")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'chat_message', 'message': message_event_obj}
            )

            # Get all users in this room group
            room = await Room.objects.aget(id=self.room_name)
            # participants_tokens = room.participants.values_list('fcm_token')
            print(room)
            api_key = os.environ.get('FCM_API_KEY')
            data_message = {
                "message_id": str(message_obj.id),
                "message": message,
                "sender": author.username,
                "room_id": str(room.id),
                "room_name": room.name
            }
            # set up  fcmpy
            print("APIKEY")
            print(api_key)
            push_service = FCMNotification(api_key=api_key)

            def get_all_fcm_tokens():
                return User.objects.filter(fcm_token__isnull=False).values_list('fcm_token', flat=True)

            # To multiple devices
            print(f"fm: {push_service}")
            fcm_tokens_func = sync_to_async(get_all_fcm_tokens)
            users_with_token = await fcm_tokens_func()

            registration_ids = []
            async for token in users_with_token:
                registration_ids.append(token)

            print(f"fmc_tokens {registration_ids}")
            print("sending push notifications...")
            try:
                result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                              data_message=data_message)
                print(f"push notifications result {result}")
            except Exception as e:
                print(str(e))
                pass

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
