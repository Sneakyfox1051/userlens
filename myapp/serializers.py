from rest_framework import serializers
from .models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['user', 'weather', 'temperature', 'location', 'wifi_ssid', 'icon_url', 'timestamp']
