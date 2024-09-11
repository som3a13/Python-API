import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config


GEOLOCATION_API_KEY = '6cedec10ca3499'
GEOLOCATION_API_URL = 'https://ipinfo.io/json'

def get_ip_location():
    try:
        response = requests.get(GEOLOCATION_API_URL, params={'token': GEOLOCATION_API_KEY})
        data = response.json()
        location = data.get('city')
        
        return location
    except Exception as e:
        return None










WEATHER_API_KEY = '7d8902ab449d7423b3ccbbf735193c84'
config = get_default_config()
config['language'] = 'en'  # Your preferred language for weather reports
owm = OWM(WEATHER_API_KEY, config)

# Get weather manager
weather_manager = owm.weather_manager()




def get_weather(location_name):
    try:
        response = requests.get(GEOLOCATION_API_URL, params={'token': GEOLOCATION_API_KEY})
        data = response.json()
        # Fetch weather data
        coords=data.get('loc').split(',')
        latitude, longitude = map(float, coords)
        print(latitude)
        print(longitude)
        observation = weather_manager.weather_at_coords(latitude, longitude)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        description = w.detailed_status
        return f"The weather in {location_name} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather data. Error: {str(e)}"


print(get_ip_location())
location_name = get_ip_location()
print(get_weather(location_name))