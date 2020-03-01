from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.index, name='index'),
    # /music/<int:album_id>/create_song
    path('<pk>/create_song/', views.create_song, name='create_song'),
    # /music/<int:album_id>/
    path('<int:album_id>/', views.detail, name='detail'),
    # /music/logout_user
    path('logout_user/', views.logout_user, name='logout_user'),
    # /music/create_album
    path('create_album/', views.create_album, name='create_album'),
    # /music/<int:album_id>/delete_song/<int:song_id>/
    path('<int:album_id>/delete_song/<int:song_id>/', views.delete_song, name='delete_song'),
    # /music/<int:album_id>/delete_album/
    path('<int:album_id>/delete_album/', views.delete_album, name='delete_album'),
    # /music/<int:album_id>/favorite_album/
    path('<int:album_id>/favorite_album/', views.favorite_album, name='favorite_album'),
    # /music/songs/--
    re_path(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    # /music/<song_id>/favorite/
    re_path(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

]
