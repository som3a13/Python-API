
import requests
from time import ctime
from gtts import gTTS
import os
import playsound
import speech_recognition as sr

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

def send_command(command):
    """Sends a command to the specified API and returns the response."""
    url = 'https://python-api-production-d196.up.railway.app/process_voice'
    response = requests.post(url, json={'command': command})
    response.raise_for_status()  # Raise HTTPError for bad responses
    return response.json()

while True:
    user_request = record()
    if user_request:
        print(f"User request: {user_request}")
        response = send_command(user_request)
        speak(response.get('response'))
        print(response.get('response'))
