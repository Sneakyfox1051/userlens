from django.urls import path
from .views import ajax_get_data, dashboard_view, login_view, register_view, get_latency_data   # Import the views

urlpatterns = [
    path('', login_view, name='login'),  # Handle root URL and redirect to the login page
    path('ajax/get-data/', ajax_get_data, name='ajax_get_data'),  # Handle AJAX requests for weather data
    path('dashboard/', dashboard_view, name='dashboard'),  # Handle dashboard page
    path('get-latency-data/', get_latency_data, name='get_latency_data'),  # Handle latency data requests
    path('register/', register_view, name='register'),  # Handle registration page
]
