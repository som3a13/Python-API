from flask import Flask, request, jsonify
from time import ctime
import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config






app = Flask(__name__)



########################################
#############APIs Tokens################
GEOLOCATION_API_KEY = '6cedec10ca3499'
GEOLOCATION_API_URL = 'https://ipinfo.io/json'

WEATHER_API_KEY = '7d8902ab449d7423b3ccbbf735193c84'
config = get_default_config()
config['language'] = 'en' 
owm = OWM(WEATHER_API_KEY, config)
weather_manager = owm.weather_manager()


def get_weather(location_name,coords):
    try:
        # Fetch weather data
        
        latitude, longitude = map(float, coords.split(','))
        observation = weather_manager.weather_at_coords(latitude, longitude)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        description = w.detailed_status
        return f"The weather in {location_name} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather data. Error: {str(e)}"
















def process_voice_command(command,location,coords):
    # Mock function to simulate voice command processing
    if "weather" in command.lower():
       
        return get_weather(location,coords)
    elif 'time' in command.lower():
          return  ctime()   
    elif 'location' in command.lower():
        return location
    else:
        return "Sorry, I didn't understand that command."

@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    command = data.get('command')
    location = data.get('location')
    coords =data.get('coords')
    latitude, longitude = map(float, coords)
    if not command:
        return jsonify({'error': 'No command provided'}), 400

    response = process_voice_command(command,location,coords)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
