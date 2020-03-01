import sys
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
import Music.views as views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('Music.urls')),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
