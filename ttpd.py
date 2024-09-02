import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)  

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

texto = "Hola, amigazos ya funciona esta porqueria."

engine.say(texto)

engine.runAndWait()

engine.save_to_file(texto, 'mensaje.mp3')
engine.runAndWait()  