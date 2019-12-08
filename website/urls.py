
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('music/', include('Music.urls')),
    path('admin/', admin.site.urls),
]
