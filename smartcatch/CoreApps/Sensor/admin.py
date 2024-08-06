from django.contrib import admin
from .models import Sensor, Alarm, Actuator

# Register your models here.
class SensorsAdmin(admin.ModelAdmin):
    list_display=("stationID","sensorName", "type", "model", "serial", "status", "notes", "min_value", "max_value")
    search_fields=("stationID","sensorName", "type", "model", "serial", "status", "notes", "min_value", "max_value")

class AlarmAdmin(admin.ModelAdmin):
    list_display = ("sensor", "timestamp", "value", "alarm_type", "message")
    search_fields = ("sensor__sensorName", "timestamp", "value", "alarm_type", "message")
    raw_id_fields = ("sensor",)
    #list_display=("sensor", "timestamp", "value", "alarm_type", "message")
    #search_fields=("sensor", "timestamp", "value", "alarm_type", "message")

class ActuatorAdmin(admin.ModelAdmin):
    list_display = ("stationID", "name", "actuators_type", "actuators_brand", "model")
    search_fields = ("stationID", "name", "actuators_type", "actuators_brand", "model")
   

admin.site.register(Sensor, SensorsAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(Actuator, ActuatorAdmin)



