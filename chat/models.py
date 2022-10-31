from django.db import models

class User(models.Model):
    name= models.CharField(max_length=12)
    def __str__(self):
        return f'{self.name}'



class Room(models.Model):
    name = models.CharField(max_length=12)
    online_users = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online_users.count()

    def join(self, user):
        self.online_users.add(user)
        self.save()

    def leave(self, user):
        self.online_users.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'



class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name}({self.room.name}): {self.content} [{self.timestamp}]'

    def get_user(self ):
        return f'{self.user.name}'

    def get_room(self ):
        return f'{self.room.name}'
