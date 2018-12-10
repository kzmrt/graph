from django.contrib import admin

from .models import Location, WeatherData

admin.site.register(Location)
admin.site.register(WeatherData)
