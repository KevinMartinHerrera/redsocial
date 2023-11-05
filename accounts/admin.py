from django.contrib import admin
from .models import User, Profile,FriendRequest


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(FriendRequest)
# Register your models here.
