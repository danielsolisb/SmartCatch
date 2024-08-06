from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
#from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
#from CoreApps.MainPage.views import index
from CoreApps.Portal.views import Dashboard, SensorListView, ReportView, AlarmListView, WarningListView, UserUpdateView

urlpatterns = [
    #path("", views.index, name="index"),
    path("Dashboard", Dashboard.as_view(), name='Dashboard'),     
    path('sensor_list/<int:pk>/', SensorListView.as_view(), name='sensor_list'),
    path('report/', ReportView.as_view(), name='report'),
    path('alarms/',  AlarmListView.as_view(), name='alarms'),
    path('warnings/',  WarningListView.as_view(), name='warnings'),
    #path('', include('django.contrib.auth.urls'), name="login"), #agregado para login
    path('logout/', include('django.contrib.auth.urls'), name="logout"), #agregado para login 
    path('edit-profile/', UserUpdateView.as_view(), name='edit_profile'),
]