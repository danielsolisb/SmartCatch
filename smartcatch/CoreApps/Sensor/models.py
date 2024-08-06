from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import BaseIterable
from django.utils.translation import templatize
from CoreApps.Station.models import Station
from datetime import date, timedelta

class Sensor(models.Model):
    stationID   =    models.ForeignKey(Station,blank=False, null=False, on_delete=models.CASCADE)
    sensorName  =    models.CharField(max_length=100, blank=True, null=True, verbose_name='SensorName')
    type        =    models.CharField(max_length=20, blank=True, null=True, verbose_name='Type')
    model       =    models.CharField(max_length=50, blank=True, null=True)
    serial      =    models.CharField(max_length=50, blank=True, null=True)
    status      =    models.CharField(max_length=20, blank=True, null=True)
    notes       =    models.TextField(max_length=100, blank=True, null=True)
    min_value   =    models.FloatField(blank=True, null=True)  # Nuevo campo para valor mínimo
    max_value   =    models.FloatField(blank=True, null=True)  # Nuevo campo para valor máximo

    def __str__(self):
        return self.sensorName

class Alarm(models.Model):
    id          = models.AutoField(primary_key=True)
    sensor      = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    value       = models.FloatField()
    alarm_type  = models.CharField(max_length=20)  # Puedes usar 'alarm' o 'warning'
    message     = models.TextField()

    def __str__(self):
        return f"{self.sensor.sensorName} - {self.timestamp} - {self.alarm_type}"

class Actuator(models.Model):
    id              =   models.AutoField(primary_key=True)
    stationID       =   models.ForeignKey(Station,blank=False, null=False, on_delete=models.CASCADE)
    name            =   models.CharField(max_length=30)
    actuators_type  =   models.CharField(max_length=20)  
    actuators_brand =   models.CharField(max_length=20)
    model           =   models.CharField(max_length=20)

    def __str__(self):
        return f"{self.stationID.name} - {self.name} - {self.actuators_type}"
