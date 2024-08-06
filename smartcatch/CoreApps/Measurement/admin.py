from django.contrib import admin
from .models import Measurements, Measurements_actuators

# Register your models here.
class MeasurementsAdmin(admin.ModelAdmin):
    list_display=("sensorID","value", "formatted_timestamp")
    search_fields=("sensorID","value", "timestamp")

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Timestamp'

class Measurements_ActuatorsAdmin(admin.ModelAdmin):
    list_display=("actuatorsID","value", "timestamp")
    search_fields=("actuatorsID","value", "timestamp")


admin.site.register(Measurements, MeasurementsAdmin)

admin.site.register(Measurements_actuators, Measurements_ActuatorsAdmin)