import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import  AsyncWebsocketConsumer

from .models import Room , Message , User


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        super().__init__()

        self.room_name = None
        self.room_group_name = None
        self.room = None

        self.user_name =None 
        self.user =None 
        self.user_inbox = None  # new
        self.isCreated  = None


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #'url_route': {'args': (), 'kwargs': {'room_name': 'mk'}}}
        self.room_group_name = f'chat_{self.room_name}'

        self.user_name = self.scope['url_route']['kwargs']['user_name'] #'url_route': {'args': (), 'kwargs': {'room_name': 'mk'}}}
        self.user_inbox = f'inbox_{self.user_name}'  # new
        
        self.user , user_iscreated  = await User.objects.get_or_create(name=self.user_name)

        self.room, self.isCreated = await Room.objects.get_or_create(name=self.room_name)
        self.room.join(self.user)

        # print(self.room.online_users.all())

        await self.accept()
        await self.channel_layer.group_add(  self.room_group_name,   self.channel_name,)

        await self.send(json.dumps({
            'type': 'user_list',
            'users': [user.name for user in self.room.online_users.all()],
        }))

        if not self.isCreated :
            await self.channel_layer.group_send(   self.room_group_name,
            {
                'type': 'user_join',
                'user_name' : self.user_name
            }
        )




    async def disconnect(self, close_code):
        print(self.user)
        self.room.leave(self.user)
        await self.channel_layer.group_discard (   self.room_group_name ,self.channel_name  )
        await self.close()




    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        print(text_data_json)

        # command = text_data_json['command']
        
        message = text_data_json['message']
        Message.objects.create(user=self.user, room=self.room, content=message)

        await self.channel_layer.group_send(     self.room_group_name,
            {
                'type': 'chat_message',
                'user_name' : text_data_json['user_name'],
                "room_name":  text_data_json['room_name'],
                'message': message,
            }
        )


    async def chat_message(self, event):
       await self.send(text_data=json.dumps(event))

    async def user_join(self, event):
      await  self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
       await self.send(text_data=json.dumps(event))



# {
#     'type': 'websocket', 
# 'path': '/ws/chat/mk/', 
# 'raw_path': b'/ws/chat/mk/',

#  'headers': [(b'host', b'127.0.0.1:8000'), (b'connection', b'Upgrade'), (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), 
#  (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'),
#   (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-version', b'13'), 
#   (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'en-US,en;q=0.9'), (b'cookie', b'csrftoken=eMdqAN72HtscDphFpAQ1KdZMFKmwt9tfNHSjGA5AW3m9prxf55zed4P9KoQM0Jnx; sessionid=e4afq0kojqtzalv4dgrgtxcxf76mu5ub'),
#    (b'sec-websocket-key', b'CIlO4y6cG+ESsNwiufmOSQ=='), (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')],
#    'query_string': b'', 
#    'client': ['127.0.0.1', 60939],
#     'server': ['127.0.0.1', 8000], 
#     'subprotocols': [],
#      'asgi': {'version': '3.0'},
#       'cookies': {'csrftoken': 'eMdqAN72HtscDphFpAQ1KdZMFKmwt9tfNHSjGA5AW3m9prxf55zed4P9KoQM0Jnx', 'sessionid': 'e4afq0kojqtzalv4dgrgtxcxf76mu5ub'}, 
#       'session': <django.utils.functional.LazyObject object at 0x000002CF2CF7B850>, 
#       'user': <channels.auth.UserLazyObject object at 0x000002CF2CF3B220>, 
#       'path_remaining': '', 

#       'url_route': {'args': (), 'kwargs': {'room_name': 'mk'}}}