from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'author', 'room', 'created_at']

    def get_author(self, obj: Message):
        return obj.author.username
