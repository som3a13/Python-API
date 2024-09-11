import requests
from time import ctime
from gtts import gTTS
import os
import playsound

def speak(txt):
    tts = gTTS(text=txt, lang='en', slow=False)
    audiofile = os.path.join(os.path.dirname(__file__), 'audio.mp3')
    tts.save(audiofile)
    playsound.playsound(audiofile)
    os.remove(audiofile)




def send_command(command):
    url = 'https://python-api-production-d196.up.railway.app/process_voice'
    response = requests.post(url, json={'command': command})
    return response.json()

# Example usage
response = send_command("What is the weather?")
speak(response['response'])

# import requests
# import json

# def fetch_data():
#     url = 'https://python-api-production-d196.up.railway.app/process_voice'
#     payload = {'command': 'What is the weather?'}
#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Request failed with status code {response.status_code}")

# def save_to_json(data, filename='response.json'):
#     with open(filename, 'w') as json_file:
#         json.dump(data, json_file, indent=4)

# if __name__ == '__main__':
#     data = fetch_data()
#     save_to_json(data)
#     print("Data saved to response.json")
