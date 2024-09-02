from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    if not text.strip():
        return "Error: No text provided.", 400

    # Convierte el texto a voz usando gTTS
    tts = gTTS(text, lang='in')  # Cambia el idioma si es necesario
    audio_file = "output.mp3"
    tts.save(audio_file)

    # Envía el archivo de audio al frontend
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


