from flask import Flask, render_template, request
import threading
from serial_reader import read_serial  
from speech_engine import speak_text, configure_speech_engine  

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ""
    
    if request.method == 'POST':
      
        texto = request.form.get('textarea')
        
        speak_text(texto)
        resultado = f"Texto hablado: {texto}"
    
    return render_template('index.html', resultado=resultado)

def start_serial_thread():
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.daemon = True 
    serial_thread.start()

if __name__ == '__main__':
    configure_speech_engine()  
    start_serial_thread()  
    app.run(debug=True)
