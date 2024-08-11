from django.shortcuts import render
from .models import ChatRoom

def chat_room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {'room_name': room_name})
