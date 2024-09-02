import serial
import pyttsx3
import speech_recognition as sr
import time
import threading

#link del boton de la web 

puerto = 'COM3'  
velocidad = 9600

engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def read_serial():
    ser = serial.Serial(puerto, velocidad)
    time.sleep(2)  

    try:
        while True:
            if ser.in_waiting > 0:
                valor = ser.readline().decode('utf-8').strip()
                print("Valor leído del pin analógico A1:", valor)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        ser.close()

from flask import Flask, request, render_template
import pyttsx3
import threading

app = Flask(__name__)

# Inicializar pyttsx3
engine = pyttsx3.init()

# Función para reproducir texto
def speak_text(texto):
    engine.say(texto)
    engine.runAndWait()

# Simulación de la lectura serial en un hilo aparte
def read_serial():
    while True:
        
        # Aquí iría el código de lectura serial
        def main():
        
        serial_thread = threading.Thread(target=read_serial)
        serial_thread.start()

        speak_text("Reproducir texto" )  
        
        rate = engine.getProperty('rate')   
        print("Tasa actual:", rate)                        
        engine.setProperty('rate', 130)      

        volume = engine.getProperty('volume')   
        print("Volumen actual:", volume)                          
        engine.setProperty('volume', 1.0)   

        voices = engine.getProperty('voices')       
        engine.setProperty('voice', voices[1].id)  
        speak_text("Mi corriente de voz actual es " + str(engine.getProperty('rate')))

        engine.save_to_file('Hola', 'probando.mp3')
        engine.runAndWait()
        pass

# Ruta principal para mostrar el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el mensaje recibido desde el formulario
@app.route('/procesar', methods=['POST'])
def procesar():
    mensaje = request.form['mensaje']
    
    # Ejecutar la lógica del main usando el texto enviado
    def main():
        serial_thread = threading.Thread(target=read_serial)
        serial_thread.start()

        speak_text(mensaje)  # Aquí utilizamos el texto recibido

        rate = engine.getProperty('rate')   
        print("Tasa actual:", rate)                        
        engine.setProperty('rate', 130)      

        volume = engine.getProperty('volume')   
        print("Volumen actual:", volume)                          
        engine.setProperty('volume', 1.0)   

        voices = engine.getProperty('voices')       
        engine.setProperty('voice', voices[1].id)  
        speak_text("Mi corriente de voz actual es " + str(engine.getProperty('rate')))

        # Guarda un archivo con la voz sintetizada
        engine.save_to_file(mensaje, 'probando.mp3')
        engine.runAndWait()

    # Llamar la función main
    main()

    # Retornar una respuesta al usuario
    return f"Mensaje procesado: {mensaje}"

if __name__ == '__main__':
    app.run(debug=True)



    
    
             