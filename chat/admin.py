from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id' ,  'name' )
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id' ,  'name' ,'get_online_count' )
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id' ,  'get_user','get_room',  'content' , 'timestamp' )

# Register your models here.
admin.site.register(User , UserAdmin)
admin.site.register(Room , RoomAdmin)
admin.site.register(Message , MessageAdmin)