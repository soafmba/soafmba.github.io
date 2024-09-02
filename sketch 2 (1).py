
const int analogPin = A1;

void setup() {

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
  
    char command = Serial.read();
    
    if (command == 'r') {
      int analogValue = analogRead(analogPin);
      

      Serial.println(analogValue);
    }
  }
}
