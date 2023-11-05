from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from PIL import Image
from django.db.models.signals import post_save


def user_directory_path_profile(instance,filename):
    profile_picture_name='users/{0}/profile.jpg'.format(instance.user.username)
    full_path=os.path.join(settings.MEDIA_ROOT,profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_picture_name

def user_directory_path_banner(instance,filename):
    profile_picture_name='users/{0}/banner.jpg'.format(instance.user.username)
    full_path=os.path.join(settings.MEDIA_ROOT,profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_picture_name

class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=50)
    facultad = models.ForeignKey('social.Facultad', on_delete=models.CASCADE, default=2)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    red_social = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.ForeignKey('social.Facultad', on_delete=models.CASCADE, default=2)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    foto_de_perfil = models.ImageField(default='users/predeterminado_perfil.png',upload_to=user_directory_path_profile)
    banner = models.ImageField(default='users/banner.jpg',upload_to=user_directory_path_banner)
    birthdate = models.DateField(blank=True, null=True)
    bio= models.TextField(max_length=150,null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)
