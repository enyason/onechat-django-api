from django.contrib import admin

from chat.models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'creator', 'created_at', 'modified_at')
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'content', 'author', 'created_at', 'modified_at')
    list_filter = ['author']
    search_fields = ['content']
