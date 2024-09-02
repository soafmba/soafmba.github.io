from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form.get('text')
    if not text or not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Convierte el texto a voz usando gTTS
        tts = gTTS(text, lang='es')  # Cambia el idioma si es necesario
        audio_file = "output.mp3"
        tts.save(audio_file)

        # Envía el archivo de audio al frontend
        response = send_file(audio_file, as_attachment=True, download_name="output.mp3")

        # Elimina el archivo después de enviarlo
        os.remove(audio_file)

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


