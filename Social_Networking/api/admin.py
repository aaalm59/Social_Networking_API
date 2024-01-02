from django.contrib import admin
from .models import FriendRequest, User,UserProfile
# Register your models here.

admin.site.register(FriendRequest)
admin.site.register(UserProfile)
