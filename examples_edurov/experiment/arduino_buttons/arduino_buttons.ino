int R1pin = A0;
int R2pin = A1;
int R3pin = A2;

int led1pin = 2;
int led2pin = 3;
int led3pin = 4;

int R1;
int R2;
int R3;

String msg;

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
  R1 = analogRead(R1pin);
  R2 = analogRead(R2pin);
  R3 = analogRead(R3pin);

  Serial.print(R1);
  Serial.print("  ");
  Serial.print(R2);
  Serial.print("  ");
  Serial.println(R3);
  delay(1000);

}
