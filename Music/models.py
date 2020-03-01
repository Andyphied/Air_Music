from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250)
    album_genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)
    album_year = models.DateField(null=True)
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self):
        return self.artist + "-" + self.album_title


class Songs(models.Model):
    albums = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    song_genre = models.CharField(max_length=100)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


