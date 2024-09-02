import serial
import pyttsx3
import threading
import time
from flask import Flask, request, render_template, send_from_directory
import os

# Configuración del puerto serial
puerto = 'COM9'  
velocidad = 9600

# Inicializar pyttsx3
engine = pyttsx3.init()

app = Flask(__name__)

# Directorio para guardar archivos de audio
AUDIO_DIR = 'audio_files'
os.makedirs(AUDIO_DIR, exist_ok=True)  # Crear el directorio si no existe

# Función para reproducir texto
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Simulación de la lectura serial en un hilo aparte
def read_serial():
    try:
        ser = serial.Serial(puerto, velocidad)
        time.sleep(2)  # Esperar a que el puerto serial esté listo

        while True:
            if ser.in_waiting > 0:
                valor = ser.readline().decode('utf-8').strip()
                print("Valor leído del pin analógico A1:", valor)
    except serial.SerialException as e:
        print(f"Error en la conexión serial: {e}")
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        ser.close()

# Función principal que se ejecutará en cada petición
def main(mensaje):
    # Iniciar el hilo de lectura serial
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.daemon = True  # El hilo se cerrará cuando termine el programa principal
    serial_thread.start()

    # Reproducir el mensaje recibido
    speak_text(mensaje)

    # Configurar las propiedades de pyttsx3
    rate = engine.getProperty('rate')
    print("Tasa actual:", rate)
    engine.setProperty('rate', 130)

    volume = engine.getProperty('volume')
    print("Volumen actual:", volume)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Usar una voz femenina (puede variar según la configuración)

    speak_text("Mi corriente de voz actual es " + str(engine.getProperty('rate')))

    # Guardar el mensaje sintetizado en un archivo
    audio_filename = os.path.join(AUDIO_DIR, 'probando.mp3')
    engine.save_to_file(mensaje, audio_filename)
    engine.runAndWait()
    
    return audio_filename

# Ruta principal para mostrar el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el mensaje recibido desde el formulario
@app.route('/procesar', methods=['POST'])
def procesar():
    mensaje = request.form['mensaje']

    # Llamar a la función main con el mensaje recibido y obtener la ruta del archivo de audio
    audio_file = main(mensaje)

    # Retornar una respuesta al usuario y el archivo de audio generado
    return f"Mensaje procesado: {mensaje}. <a href='/download/{os.path.basename(audio_file)}'>Descargar archivo de audio</a>"

# Ruta para servir el archivo de audio
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
    
