from django.shortcuts import render

from chat.models import Room,User

# import redis

def index_view(request):
    # Connect to our Redis instance
    # redis_instance = redis.StrictRedis(host='127.0.0.1',        port=6379, db=0)
    # print(redis_instance)
    # print(Room.objects.all())

    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name , user_name):
 
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user_name': user_name,
    })

