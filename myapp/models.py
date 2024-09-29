from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Create your models here.
class WeatherData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming Aditi's user ID is 1
    weather = models.CharField(max_length=250)
    temperature = models.FloatField(default=0.0)
    location = models.CharField(max_length=100, default="Unknown location")
    wifi_ssid = models.CharField(max_length=100, default="Unknown Wi-Fi")  # New field
    icon_url = models.URLField(max_length=200, blank=True, null=True)  # Add this line
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}: {self.weather} - {self.temperature}°C (Wi-Fi: {self.wifi_ssid})"
