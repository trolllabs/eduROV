double kPaRead(int pin) {
  //Read and convert analog value to atmospheric pressure
  double val = analogRead(pin);
  double vo = 5.0 * (val / 1023);
  double p = 250 * (vo / 5) + 10;
  return p;
}

double getTemp(int pin) {
  //Reading temperature sensor lm35 at analogpin "pin"
  double tempVals = 0;
  for(int i = 0; i < 10; i++){
    tempVals += (500.0*analogRead(pin))/1024;
  }
  double temp = tempVals/10.0;
  return temp;
  
}

double getVolt(int pin){
  //Read battery voltage value from "pin"
  //Convert to voltage
  //Multiply by 2, since the PCB has an onboard voltage divider to make the voltage readable by the Arduino ADC
  return (((5.0*analogRead(pin))/1023)*2);
}

void printSensorValues(){
  //message is started with the number of bytes available in the message
  //All values are separated by a colon ":", including the message length
  String msg = String(temp) + ':' + String(pressure) + ':' + String(battVolt);
  
  send_signal(msg);
  //int len = msg.length() + 1;
  //msg = String(len) + ":" + msg;
  //Serial.println(msg);
}

