import requests

def send_command_to_internal_service(command):
    url = 'python-api-production-d196.up.railway.app/process_voice'
    response = requests.post(url, json={'command': command})
    return response.json()

# Example usage
response = send_command_to_internal_service("What is the weather?")
print(response['response'])
