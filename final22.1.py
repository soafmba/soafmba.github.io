import serial
import pyttsx3
import threading
import time
import gpiozero
from   flask import Flask, request, render_template
from   keyboard import is_pressed


puerto = 'COM9'  
velocidad = 9600

# Inicializar pyttsx3
engine = pyttsx3.init()

app = Flask(__name__)

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
    engine.save_to_file(mensaje, 'probando.mp3')
    engine.runAndWait()

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

# Setup the PWM pin
pwm_output = gpiozero.PWMOutputDevice(18)  # Connect to GPIO18 (you can change to your pin)

try:
    while True:
        if is_pressed('1'):  # If key '1' is pressed
            pwm_output.value = 1.0  # Send 100% PWM signal (simulate 5V)
        else:
            pwm_output.value = 0.0  # Turn off the signal
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Program terminated")

finally:
    pwm_output.close()  # Cleanup

