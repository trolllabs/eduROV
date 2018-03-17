int bluePin = 2;
int greenPin = 3;
int redPin = 4;
int yellowPin = 5;
unsigned long last_send;

void send_signal(String msg);
String receive_signal();
String int_to_hex(int num, int precision);
String read_sensors();
void control_motors(String commands);

void setup() {
  Serial.begin(115200);
  pinMode(bluePin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    control_motors(receive_signal());
  }
  if (millis() - last_send >= 500) {
    send_signal(read_sensors());
    last_send = millis();
  }
}

void control_motors(String commands) {
  // Commands in format "0120"
  
  int blue = String(commands[0]).toInt();
  int green = String(commands[1]).toInt();
  int red = String(commands[2]).toInt();
  int yellow = String(commands[3]).toInt();
  digitalWrite(bluePin, blue);
  digitalWrite(greenPin, green);
  digitalWrite(redPin, red);
  digitalWrite(yellowPin, yellow);
}

String read_sensors() {
  // Returns string in format "42.0:2.175:1"
  
  float pressure = 45.2;
  float temp = 27.457;
  int value = 1;

  String str = "";
  str += pressure;
  str += ':';
  str += temp;
  str += ':';
  str += value;
  return str;
}

