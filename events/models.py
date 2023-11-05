from django.db import models
from social.models import Facultad
from accounts.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    participants = models.ManyToManyField(User, related_name='events_participating')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    faculty = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)  # Por defecto, el evento no está aceptado

    def __str__(self):
        return self.title