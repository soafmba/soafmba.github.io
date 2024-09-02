
import serial
import pyttsx3
import speech_recognition as sr
import time
import threading

puerto = 'COM8'  
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

def main():
    
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.start()

    speak_text("Reproducir texto" ) #link de sofi
    
    rate = engine.getProperty('rate')   
    print("Tasa actual:", rate)                        
    engine.setProperty('rate', 130)      

    volume = engine.getProperty('volume')   
    print("Volumen actual:", volume)                          
    engine.setProperty('volume', 1.0)   

    voices = engine.getProperty('voices')       
    engine.setProperty('voice', voices[1].id)  
    speak_text("Mi corriente de voz actual es " + str(engine.getProperty('rate')))

    engine.save_to_file('Hola', 'probando.mp3')#link de chofi
    engine.runAndWait()

if __name__ == "__main__":
    main()


