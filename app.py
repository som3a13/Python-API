from flask import Flask, request, jsonify
from time import ctime
import pyowm
from geopy.geocoders import Nominatim






app = Flask(__name__)




WEATHER_API_KEY = '7d8902ab449d7423b3ccbbf735193c84'
owm = pyowm.OWM(WEATHER_API_KEY)  

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapiExercises")


def get_weather(location_name):
    try:
        # Geocode the location
        location = geolocator.geocode(location_name)
        if not location:
            return "Sorry, I couldn't find that location."

        # Fetch weather data
        observation = owm.weather_at_coords(location.latitude, location.longitude)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']
        description = w.get_status()
        return f"The weather in {location_name} is {description} with a temperature of {temp}°C."
    except pyowm.commons.exceptions.APIRequestError as e:
        return f"Sorry, I couldn't fetch the weather data. Error: {str(e)}"
















def process_voice_command(command):
    # Mock function to simulate voice command processing
    if "weather" in command.lower():
        return "The weather today is sunny with a high of 25°C."
    elif 'time' in command.lower():
          return  ctime()   
    elif  "location" in command.lower():
        location_name = command.lower().split('weather', 1)[1].strip()
        return get_weather(location_name)
    else:
        return "Sorry, I didn't understand that command."

@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    command = data.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400

    response = process_voice_command(command)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
