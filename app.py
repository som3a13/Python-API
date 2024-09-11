from flask import Flask, request, jsonify
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pytz import timezone
from timezonefinder import TimezoneFinder
from datetime import datetime





app = Flask(__name__)



########################################
#############APIs Tokens################
WEATHER_API_KEY = '7d8902ab449d7423b3ccbbf735193c84'
config = get_default_config()
config['language'] = 'en' 
owm = OWM(WEATHER_API_KEY, config)
weather_manager = owm.weather_manager()


def get_weather(location_name,coords):
    try:
        # Fetch weather data
        
        latitude, longitude = map(float, coords)
        observation = weather_manager.weather_at_coords(latitude, longitude)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        description = w.detailed_status
        return f"The weather in {location_name} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather data. Error: {str(e)}"


def get_local_time(coords):
    """Fetches the local time based on provided location coordinates."""
    try:
        latitude, longitude = map(float, coords)
        tf = TimezoneFinder()
        # Find the timezone based on the coordinates
        tz = tf.timezone_at(lng=longitude, lat=latitude)
        local_time = datetime.now(timezone(tz)).strftime('%a %b %d %H:%M:%S %Y')
        return f"Today is  {local_time}."
    except Exception as e:
        return f"Could not determine the local time. Error: {str(e)}"










def process_voice_command(command,location,coords):
    # Mock function to simulate voice command processing
    if "weather" in command.lower():
        return get_weather(location,coords)
    elif 'time' in command.lower():
          return  get_local_time(coords)
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

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    response = process_voice_command(command,location,coords)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
