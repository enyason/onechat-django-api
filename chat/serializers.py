from rest_framework import serializers

from chat.models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'author', 'room', 'created_at']

    def get_author(self, obj: Message):
        return obj.author.username


class RoomSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'creator', 'name', 'created_at']

    def get_creator(self, obj: Room):
        return obj.creator.username
