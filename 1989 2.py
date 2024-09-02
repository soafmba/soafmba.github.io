from flask import Flask, request, render_template
import threading
import pyttsx3
import serial
import time

# Iniciacion del modulo pyttsx3
engine = pyttsx3.init()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-command', methods=['POST'])

def send_command():
    command = request.form['command']
    # Logic to send the command to the Arduino or perform TTS
    send_command_to_arduino(command, arduino_serial)
    speak_text(command)
    return "Command Sent", 200


def speak_text(text):
    """convertir texto a voz usandopyttsx3."""
    engine.say(text)
    engine.runAndWait()
     

def send_command_to_arduino(command, arduino_serial):
    """enviar comandos de arduino para controlar reles."""
    arduino_serial.write((command + '\n').encode('utf-8'))

def read_serial(port, arduino_serial):
    """leer del puerto serial dado y reproducir comandos."""
    try:
        with serial.Serial(port, 9600, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    print(f"Data from {port}: {data}")
                    speak_text(data)
                    
                    #enviar datos al arduino
                    send_command_to_arduino(data, arduino_serial)
                    
                time.sleep(1)  
    except serial.SerialException as e:
        print(f"Error reading from {port}: {e}")

def main(mensaje):
    # abrir la conexion con la placa de arduino
    arduino_port = '/dev/ttyUSB0'  
    arduino_serial = serial.Serial(arduino_port, 9600, timeout=1)
    
    #puertos seriales
    ports = ['/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5', '/dev/ttyS6']
    
    for port in ports:
        serial_thread = threading.Thread(target=read_serial, args=(port, arduino_serial))
        serial_thread.daemon = True  
        serial_thread.start()
    
    # Configuracion demodulo pyttsx3
    rate = engine.getProperty('rate')
    print("Current rate:", rate)
    engine.setProperty('rate', 130)

    volume = engine.getProperty('volume')
    print("Current volume:", volume)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  #voz utilizada
    else:
        print("No disponibles voces alternativas.")

    # reproducir mensaje
    speak_text(mensaje)

    # anunciar corriente de voz
    speak_text("corriente de voz actual" + str(engine.getProperty('rate')))

    # 
    engine.save_to_file(mensaje, 'probando.mp3')
    engine.runAndWait()

    # Close serial connection to Arduino
    arduino_serial.close()

if __name__ == "__main__":
    mensaje = "Hola, este es un mensaje de prueba."
    main(mensaje)
