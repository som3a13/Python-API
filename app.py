from flask import Flask, request, jsonify

app = Flask(__name__)

def process_voice_command(command):
    # Mock function to simulate voice command processing
    if "weather" in command.lower():
        return "The weather today is sunny with a high of 25°C."
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
