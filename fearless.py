from flask import Flask, request, render_template, redirect, url_for
import pyttsx3

app = Flask(__name__)

# Inicializar el motor de pyttsx3
engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    mensaje = request.form.get('mensaje')

    if mensaje:
        # Convertir texto a voz
        engine.say(mensaje)
        engine.runAndWait()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


