from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import WeatherDataSerializer
from .models import WeatherData
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
import requests
from .utils import get_wifi_ssid, get_network_latency  # Import the get_network_latency function
from django.contrib.auth.decorators import login_required
import time

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Get the latitude and longitude from the form
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            # Store the latitude and longitude in the session for later use
            request.session['latitude'] = latitude
            request.session['longitude'] = longitude
            
            return redirect('dashboard')  # Redirect to the dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@api_view(['GET'])
def ajax_get_data(request):
    api_key = 'c983bc9e705ecb470e33691bffa93759'
    
    # Retrieve latitude and longitude from the session
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    
    if latitude and longitude:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=en'
    else:
        city = 'Chandigarh'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        temperature = data.get('main', {}).get('temp', 'N/A')
        weather_description = data.get('weather', [{}])[0].get('description', 'N/A')
        location = data.get('name', 'Unknown location')
        icon_code = data.get('weather', [{}])[0].get('icon', '01d')  # Default to a clear sky icon if not present
        
        # Construct the icon URL
        icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'
        
        # Retrieve Wi-Fi SSID
        wifi_ssid = get_wifi_ssid()
        
        # Save to the database
        WeatherData.objects.create(
            weather=weather_description,
            temperature=temperature,
            location=location,
            wifi_ssid=wifi_ssid,  # Save Wi-Fi SSID in the database
            icon_url=icon_url    # Save the icon URL in the database
        )
        
        return JsonResponse({
            'temperature': temperature,
            'weather': weather_description,
            'location': location,
            'wifi_ssid': wifi_ssid,  # Send Wi-Fi SSID in the response
            'icon_url': icon_url    # Send icon URL in the response
        })
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


# New view to capture and send network latency data
@api_view(['GET'])
def get_latency_data(request):
    latency_data = []
    
    # Capture network latency multiple times to simulate real-time data
    for _ in range(10):  # Capture 10 samples
        latency = get_network_latency()
        if latency is not None:
            latency_data.append(latency)
        time.sleep(1)  # Wait for 1 second between pings

    return JsonResponse({'latency': latency_data})


@login_required
def dashboard_view(request):
    # Ensure that the user is logged in before rendering the dashboard
    return render(request, 'dashboard.html', {'user': request.user})
