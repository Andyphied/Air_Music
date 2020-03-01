from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Songs


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg', 'flac', 'acc', 'm4a']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            file_type = album.album_logo.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                response = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', response)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        response = {
            "form": form,
        }
        return render(request, 'music/create_album.html', response)



def create_song(request, pk):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=pk)
    if form.is_valid():
        album_songs = album.songs_set.all()
        for s in album_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                response = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', response)
        song = form.save(commit=False)
        song.albums = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            response = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, Flac, ACC, or OGG',
            }
            return render(request, 'music/create_song.html', response)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    response = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', response)



def delete_album(request, album_id):
    album = Album.objects.get(pk = album_id)
    album.delete()
    albums = Album.objects.filter(user =request.user)
    return render (request, 'music/index.html', {'albums':albums})



def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Songs.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})



def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})



def favorite(request, song_id):
    song = get_object_or_404(Songs, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Songs.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Songs.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    response = {
        "form": form,
    }
    return render(request, 'music/login.html', response)



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    response = {
        "form": form,
    }
    return render(request, 'music/register.html', response)



def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.songs_set.all():
                    song_ids.append(song.pk)
            users_songs = Songs.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'songs_list': users_songs,
            'filter_by': filter_by,
        })


