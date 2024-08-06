from django.contrib import admin
from .models import Station

# Register your models here.
class StationAdmin(admin.ModelAdmin):
    list_display=("name", "address", "telephone", "coordinates")
    search_fields=("name", "address", "telephone", "coordinates")

admin.site.register(Station, StationAdmin)