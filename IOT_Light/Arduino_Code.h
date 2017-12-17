
//Arduino程序，通过简单的判断实现

String comchar;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while (Serial.available() > 0) {
    comchar = Serial.read();
    Serial.print("Serial.read: ");
    Serial.println(comchar);
    delay(100);

    if (comchar == "79") {
      digitalWrite(13, HIGH);
      Serial.println("open");
    }
    if (comchar == "78") {
      digitalWrite(13, LOW);
      Serial.println("close");
    }
  }
}
