from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
#from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
#from CoreApps.MainPage.views import index
from CoreApps.MainPage import views
from CoreApps.MainPage.views import main, about, agroIoT, avicolaIoT, industrial, demoRequest, acuicultura
from CoreApps.MainPage import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", main.as_view(), name='mainpage'),
    path("about", about.as_view(), name='about'),
    path("contact", views.contact, name='contact'),
    path("demoRequest", views.demoRequest, name='Demo'),
    path('agroIOT', agroIoT.as_view(), name='agroiot'),
    path('avicolaIOT', avicolaIoT.as_view(), name='avicolaiot'),
    path('industrial', industrial.as_view(), name='industrial'),
    path('acuicultura', acuicultura.as_view(), name='acuicultura')
    
]