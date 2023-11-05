from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Facultad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

def user_directory_path(instance,filename):
    return 'user/socialpost{0}'.format(filename)
    
""" def dm_directory_path(instance,filename):
    return 'user/messages{0}'.format(filename) """

class SocialPost(models.Model):
    body= models.TextField()
    image= models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='social_post_author')
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes =  models.ManyToManyField(User,blank=True,related_name='dislikes')

class SocialComments(models.Model):
    comment = models.TextField(default="valor de comentario")
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_comment_author')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='comments', default=0)



class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
   



