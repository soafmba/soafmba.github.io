import pyttsx3
from flask import Flask, request, render_template

# Inicializar pyttsx3
engine = pyttsx3.init()

# Configuración inicial de pyttsx3 (utilizará el audio del PC)
engine.setProperty('rate', 130)  # Ajustar la velocidad de habla
engine.setProperty('volume', 1.0)  # Volumen máximo

# Selección de voz (ajuste según las voces instaladas en el sistema)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Usar voz femenina

app = Flask(__name__)

# Función para reproducir texto usando los parlantes del PC
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Función principal que se ejecutará en cada petición
def main(mensaje):
    # Reproducir el mensaje recibido (por el audio del PC)
    speak_text(mensaje)

# Ruta principal para mostrar el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el mensaje recibido desde el formulario
@app.route('/procesar', methods=['POST'])
def procesar():
    mensaje = request.form['mensaje']

    # Llamar a la función main con el mensaje recibido
    main(mensaje)

    # Retornar una respuesta al usuario
    return f"Mensaje procesado: {mensaje}"

if __name__ == '__main__':
    app.run(debug=True)
