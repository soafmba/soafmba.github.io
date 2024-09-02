from flask import Flask, request, render_template
import threading
import pyttsx3
import serial
import time

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

app = Flask(__name__)

# Global variable for Arduino serial connection
arduino_serial = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-command', methods=['POST'])
def send_command():
    command = request.form['command']
    if arduino_serial and arduino_serial.is_open:
        # Send command to Arduino
        send_command_to_arduino(command, arduino_serial)
        # Speak the command via TTS
        speak_text(command)
        return "Command Sent", 200
    else:
        return "Arduino Not Connected", 500

def speak_text(text):
    """Convert text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def send_command_to_arduino(command, arduino_serial):
    """Send command to Arduino via serial."""
    arduino_serial.write((command + '\n').encode('utf-8'))

def read_serial(port, arduino_serial):
    """Continuously read from the given serial port and speak incoming data."""
    try:
        with serial.Serial(port, 9600, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    print(f"Data from {port}: {data}")
                    speak_text(data)

                    # Optionally send data to the Arduino
                    send_command_to_arduino(data, arduino_serial)

                time.sleep(1)
    except serial.SerialException as e:
        print(f"Error reading from {port}: {e}")

def initialize_arduino_connection():
    global arduino_serial
    arduino_port = '/dev/ttyUSB0'  # Update with the correct port
    try:
        # Open serial connection with Arduino
        arduino_serial = serial.Serial(arduino_port, 9600, timeout=1)
        print(f"Connected to Arduino on {arduino_port}.")
    except serial.SerialException as e:
        print(f"Error: Unable to connect to Arduino. {e}")
        arduino_serial = None

def start_serial_reading():
    """Start a background thread to read from multiple serial ports."""
    ports = ['/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3']  # Adjust to your setup

    for port in ports:
        serial_thread = threading.Thread(target=read_serial, args=(port, arduino_serial))
        serial_thread.daemon = True  # This ensures the thread will exit when the main program exits
        serial_thread.start()

def main():
    mensaje = "Hola, este es un mensaje de prueba."

    # Initialize Arduino connection
    initialize_arduino_connection()

    if arduino_serial:
        # Start background serial reading
        start_serial_reading()

        # Configure pyttsx3 settings
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Use alternative voice if available

        # Speak the initial message
        speak_text(mensaje)

    else:
        print("Arduino connection not established. Cannot proceed with serial reading or TTS.")

if __name__ == "__main__":
    # Start the background tasks (serial reading)
    main()

    # Start the Flask web app
    app.run(host="0.0.0.0", port=5000, debug=True)
