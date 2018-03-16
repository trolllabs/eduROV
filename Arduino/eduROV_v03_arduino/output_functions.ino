void updateOutput(String msg) {
  // expects a 4 digit string, values 0, 1 or 2

  //Diving/rising motors
  //Run two motors in sync
  if (msg[0] == '1') {
    digitalWrite(ch1a, HIGH);
    digitalWrite(ch1b, LOW);
    digitalWrite(ch2a, HIGH);
    digitalWrite(ch2b, LOW);
  } else if (msg[0] == '2') {
    digitalWrite(ch1a, LOW);
    digitalWrite(ch1b, HIGH);
    digitalWrite(ch2a, LOW);
    digitalWrite(ch2b, HIGH);
  } else {
    digitalWrite(ch1a, LOW);
    digitalWrite(ch1b, LOW);
    digitalWrite(ch2a, LOW);
    digitalWrite(ch2b, LOW);
  }

  //Port side motor
  if(msg[1] == '1'){
    digitalWrite(ch3a, HIGH);
    digitalWrite(ch3b, LOW);
  }else if(msg[1] == '2'){
    digitalWrite(ch3a, LOW);
    digitalWrite(ch3b, HIGH);
  }else{
    digitalWrite(ch3a, LOW);
    digitalWrite(ch3b, LOW);
  }
  //Starboard motor
  if(msg[2] == '1'){
    digitalWrite(ch4a, HIGH);
    digitalWrite(ch4b, LOW);
  }else if(msg[2] == '2'){
    digitalWrite(ch4a, LOW);
    digitalWrite(ch4b, HIGH);
  }else{
    digitalWrite(ch4a, LOW);
    digitalWrite(ch4b, LOW);
  }

  //LED lights
  if(msg[3] == '1'){
    digitalWrite(ledPin, HIGH);
  }else{
    digitalWrite(ledPin, LOW);
  }
}

