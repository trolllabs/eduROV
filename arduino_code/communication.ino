void send_signal(String msg) {
  // Adds length of msg in hex format to msg and sends it
  
  String len = int_to_hex(msg.length(), 4);
  Serial.println(len + msg);
}

String receive_signal() {
  // Returns string in format "0120"
  
  delay(5); // Let the whole string arrive to buffer
  char inData[100]; // Allocate some space for the string
  char inChar; // Where to store the character read
  byte index = 0; // Index into array; where to store the character
  // Read in a whole string
  while (Serial.available() > 0) {
    inChar = Serial.read(); // Read a character
    inData[index] = inChar; // Store it
    index++; // Increment where to write next
    inData[index] = '\0'; // Null terminate the string
  }
  // Remove first 6 characters which describes the length
  String str = String(inData);
  return str.substring(6);
}

String int_to_hex(int num, int precision) {
  // Returns string in format "0x01fb"
  
  char tmp[16];
  char format[128];
  sprintf(format, "0x%%.%dX", precision);
  sprintf(tmp, format, num);
  return tmp;
}
