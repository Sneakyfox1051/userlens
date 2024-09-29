from django.contrib import admin

# Register your models here.
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'weather', 'temperature', 'location')  # Display all relevant fields
    search_fields = ('weather', 'location')  # Allow searching by weather and location
    list_filter = ('timestamp', 'location')  # Filter by timestamp and location for easier navigation
