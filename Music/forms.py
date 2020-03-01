from django import forms
from django.contrib.auth.models import User
from .models import Album, Songs

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'album_genre', 'album_logo', 'album_year']


class SongForm(forms.ModelForm):
    
    class Meta:
        model = Songs
        fields = ['song_title', 'audio_file', 'song_genre']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
