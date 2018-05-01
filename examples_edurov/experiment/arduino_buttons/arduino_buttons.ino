int R1pin = A0;
int R2pin = A1;
int R3pin = A2;

int led1pin = 2;
int led2pin = 3;
int led3pin = 4;

int R1;
int R2;
int R3;
int analog;

String msg;
int threshold = 900;
int lastButton = 0;
int newButton = 0;

int success(int button);
void light_leds(int button);

void setup() {
  pinMode(R1pin, INPUT);
  pinMode(R2pin, INPUT);
  pinMode(R3pin, INPUT);

  pinMode(led1pin, OUTPUT);
  pinMode(led2pin, OUTPUT);
  pinMode(led3pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (success(newButton)) {
    lastButton = newButton;
    while (newButton == lastButton) {
      newButton = random(0, 3);
    }
  }
  light_leds(newButton);
  delay(50);
}

int success(int button) {
  int result = false;
  if (button == 0) {
    analog = analogRead(R1pin);
  } else if (button == 1) {
    analog = analogRead(R2pin);
  } else if (button == 2) {
    analog = analogRead(R3pin);
  }
  if (analog >= threshold) {
    result = true;
    Serial.println("hit="+(String)button);
  } 
  return result;
}

void light_leds(int button) {
  if (button == 0) {
    digitalWrite(led1pin, HIGH);
    digitalWrite(led2pin, LOW);
    digitalWrite(led3pin, LOW);
  } else if (button == 1) {
    digitalWrite(led1pin, LOW);
    digitalWrite(led2pin, HIGH);
    digitalWrite(led3pin, LOW);
  } else if (button == 2) {
    digitalWrite(led1pin, LOW);
    digitalWrite(led2pin, LOW);
    digitalWrite(led3pin, HIGH);
  }
}

