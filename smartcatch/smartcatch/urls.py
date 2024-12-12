from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from . import settings
from users.views import register

from CoreApps.MainPage.views import page_not_found404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("CoreApps.MainPage.urls")),
    path("Portal/", include("CoreApps.Portal.urls")),
    path("Register", register, name="register" )    
]

handler404 = page_not_found404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)