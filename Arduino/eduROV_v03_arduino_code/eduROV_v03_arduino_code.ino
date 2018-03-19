/*
   eduROV Arduino code
   Handles:
   - Motor controls
   - External temperature sensor
   - External pressure sensor
   - Battery voltage measurement
   - LED lanterns
   - Serial communications to the eduROV python server

   Provided as-is and free to be modified as you see fit.
*/

//Sensor pins:
#define pressPin A0
#define tempPin A1
#define battVoltPin A2

//Motor control pins
// the rise/dive motors are run syncronized, they represent one linear axis of movement
#define ch1a 12  //rise/dive
#define ch1b 11  //rise/dive
#define ch2a 10  //rise/dive
#define ch2b 9   //rise/dive
#define ch3a 8   //port motor
#define ch3b 7   //port motor
#define ch4a 6   //starboard motor
#define ch4b 5   //starboard motor

//Other peripherals
#define ledPin 13

//Communication variables
String input = " ";
String output = " ";

unsigned long messageTime = 0;
unsigned int delayTime = 100; //how long between each sensor update - milliseconds

//Sensor variables
volatile double pressure = 0;
volatile double temp = 0;
volatile double battVolt = 0;

void setup() {
  Serial.begin(115200);

  //Pinmode definitions
  pinMode(ch1a, OUTPUT);
  pinMode(ch1b, OUTPUT);
  pinMode(ch2a, OUTPUT);
  pinMode(ch2b, OUTPUT);
  pinMode(ch3a, OUTPUT);
  pinMode(ch3b, OUTPUT);
  pinMode(ch4a, OUTPUT);
  pinMode(ch4b, OUTPUT);
  pinMode(ledPin, OUTPUT);

  //Turn everything off
  digitalWrite(ch1a, LOW);
  digitalWrite(ch1b, LOW);
  digitalWrite(ch2a, LOW);
  digitalWrite(ch2b, LOW);
  digitalWrite(ch3a, LOW);
  digitalWrite(ch3b, LOW);
  digitalWrite(ch4a, LOW);
  digitalWrite(ch4b, LOW);

  digitalWrite(ledPin, LOW);

}

void loop() {
  //Serial read
  if (Serial.available() > 0) {
    input = receive_signal();
    //Test print to verify input, use for debugging only
    //Serial.println(input);
  }

  //Reading sensors
  pressure = kPaRead(pressPin);
  temp = getTemp(tempPin);
  battVolt = getVolt(battVoltPin);
  
  if ((millis() - messageTime) > delayTime) {
    messageTime = millis();
    printSensorValues();
  }
  updateOutput(input);

}
