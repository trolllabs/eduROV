int R0pin = A0;
int R1pin = A1;
int R2pin = A2;

int led0pin = 2;
int led1pin = 3;
int led2pin = 4;

//int R1;
//int R2;
//int R3;
//int analog;

String msg;
int threshold0 = 620;
int threshold1 = 810;
int threshold2 = 780;
int lastButton = 0;
int newButton = 0;

int success(int button);
void light_leds(int button);

void setup() {
  pinMode(R0pin, INPUT);
  pinMode(R1pin, INPUT);
  pinMode(R2pin, INPUT);

  pinMode(led0pin, OUTPUT);
  pinMode(led1pin, OUTPUT);
  pinMode(led2pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (success(newButton)) {
    lastButton = newButton;
    while (newButton == lastButton) {
      newButton = random(0, 3);
    }
    Serial.println(newButton);
  }
  light_leds(newButton);
  delay(50);
}

int success(int button) {
  int result = false;
//  Serial.print(analogRead(R0pin));
//  Serial.print("  ");
//  Serial.print(analogRead(R1pin));
//  Serial.print("  ");
//  Serial.println(analogRead(R2pin));
  if (button == 0) {
    if (analogRead(R0pin) >= threshold0) {
      result = true;
    } 
  } else if (button == 1) {
    if (analogRead(R1pin) >= threshold1) {
      result = true;
    } 
  } else if (button == 2) {
    if (analogRead(R2pin) >= threshold2) {
      result = true;
    } 
  }
  if (result) {
    Serial.println("hit="+(String)button);
  } 
  return result;
}

void light_leds(int button) {
  if (button == 0) {
    digitalWrite(led0pin, HIGH);
    digitalWrite(led1pin, LOW);
    digitalWrite(led2pin, LOW);
  } else if (button == 1) {
    digitalWrite(led0pin, LOW);
    digitalWrite(led1pin, HIGH);
    digitalWrite(led2pin, LOW);
  } else if (button == 2) {
    digitalWrite(led0pin, LOW);
    digitalWrite(led1pin, LOW);
    digitalWrite(led2pin, HIGH);
  }
}

