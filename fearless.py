
from flask import Flask, request, jsonify
import pyttsx3

app = Flask(__name__)

# Inicializa el motor pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)  
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.json
    texto = data.get('text', '')

    # Convertir texto a voz y guardarlo en un archivo MP3
    engine.say(texto)
    engine.save_to_file(texto, 'static/mensaje.mp3')
    engine.runAndWait()

    return jsonify({"message": "Command processed", "audio_file": "mensaje.mp3"}), 200

if __name__ == "__main__":
    app.run(debug=True)
