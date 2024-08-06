from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import BaseIterable
from django.utils.translation import templatize
from CoreApps.Sensor.models import Sensor, Actuator
# Create your models here.

class Measurements (models.Model):
    id          = models.AutoField(primary_key=True)
    sensorID    = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name="Associated Sensor")
    value       = models.FloatField(verbose_name="Data")
    timestamp   = models.DateTimeField(auto_now_add=True)

    def formatted_value(self):
        # Formatear el valor para mostrar 7 dígitos enteros y 2 decimales
        return "{:.2f}".format(self.value)
    
    def __str__(self):
        return f"{self.sensorID.sensorName} - {self.value} - {self.timestamp}"
    
    class Meta:
        indexes = [
            models.Index(fields=['sensorID']),
            models.Index(fields=['timestamp']),
        ]

class Measurements_actuators(models.Model):
    id          = models.AutoField(primary_key=True)
    actuatorsID = models.ForeignKey(Actuator, on_delete=models.CASCADE, verbose_name="Associated Actuators")
    value       = models.FloatField(verbose_name="Data")
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actuatorsID.name} - {self.value} - {self.timestamp}"

