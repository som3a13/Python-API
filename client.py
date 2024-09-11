
import requests
from time import ctime
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
import subprocess


def speak(txt):
    """Converts the provided text to speech using gTTS."""
    try:
        tts = gTTS(text=txt, lang='en', slow=False)
        audiofile = os.path.join(os.path.dirname(__file__), 'audio.mp3')
        tts.save(audiofile)
        playsound.playsound(audiofile)
    finally:
        # Ensure the audio file is removed even if an error occurs
        if os.path.exists(audiofile):
            os.remove(audiofile)

def record(order=None, timeout=None):
    """Captures audio from the microphone and recognizes speech."""
    recognizer = sr.Recognizer()

    if order:
        speak(order)

    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=timeout)  # Record audio with the specified timeout
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

    print("Recognizing...")
    try:
        # Recognize the audio using Google Web Speech API
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Error connecting to the Google Web Speech API: {e}")
        return None



GEOLOCATION_API_KEY = '6cedec10ca3499'
GEOLOCATION_API_URL = 'https://ipinfo.io/json'

def get_ip_location():
    try:
        response = requests.get(GEOLOCATION_API_URL, params={'token': GEOLOCATION_API_KEY})
        data = response.json()
        location = data.get('city') + ', ' + data.get('country')
        coords=data.get('loc').split(',')
        return location,coords
    except Exception as e:
        return None








def send_command(command,location,coords):
    """Sends a command to the specified API and returns the response."""
    url = 'https://python-api-production-d196.up.railway.app/process_voice'
    response = requests.post(url, json={'command': command, 'location': location, 'coords' : coords})
    response.raise_for_status()  # Raise HTTPError for bad responses
    return response.json()







def execute_local_command(command):
    """Executes a local command on the client machine."""
    try:
        if 'terminal' in command.lower():
            # Example command to open a terminal (this may vary based on your OS)
            subprocess.Popen(['gnome-terminal'])  # For Linux with GNOME
            return "Terminal opened."
        elif 'firefox' in command.lower():
            subprocess.Popen(['firefox'])
            return "firefox opened."
        
        else:
            return "Local command not recognized."
    except Exception as e:
        return f"Error executing local command: {str(e)}"
    



while True:
    user_request = record()
    if user_request:
        print(f"User request: {user_request}")
        location, coords = get_ip_location()
        if 'run' in user_request.lower():
            # Handle local command directly
            local_response = execute_local_command(user_request)
            speak(local_response)
            print(local_response)
        else:
            # Send command to server
            response = send_command(user_request, location, coords)
            speak(response.get('response'))
            print(response.get('response'))
