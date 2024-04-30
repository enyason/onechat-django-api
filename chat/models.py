import uuid as uuid
from django.db import models
from django.utils import timezone

from users.models import User


class Room(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='user_rooms')
    name = models.CharField(max_length=64, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
