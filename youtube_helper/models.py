from django.db import models

# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
  
class Playlist(models.Model):
    playlist_id = models.CharField(max_length=100)
    playlist_length = models.CharField(max_length=100)

class Transcript(models.Model):
    video_id = models.CharField(max_length=100)
    video_text = models.TextField()