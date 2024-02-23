String readString;

void setup() {
  Serial.begin(115200);
  Serial.println("serial test 0021"); // so I can keep track of what is loaded

  pinMode(13,OUTPUT);
  pinMode(A0,OUTPUT);
  digitalWrite(A0,LOW);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      // Newline character encountered, print the received string
      if (readString.length() > 0) {
        Serial.println(readString);
        readString = "";
      }
    } else {
      // Append the character to the string
      readString += c;
    }
  }
  if (readString == "Received command: Bye"){
    digitalWrite(13,HIGH);
  }else if (readString == "Received command: Hello"){
    digitalWrite(13,LOW);
  }
}
