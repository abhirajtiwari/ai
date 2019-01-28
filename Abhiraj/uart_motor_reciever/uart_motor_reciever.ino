int lf = 4;
int lb = 2;
int le = 3;

int rf = 10;
int rb = 8;
int re = 9;

void setup() {
  Serial.begin(115200);
  pinMode(lf, OUTPUT);
  pinMode(rf, OUTPUT);
  pinMode(lb, OUTPUT);
  pinMode(rb, OUTPUT);
  pinMode(le, OUTPUT);
  pinMode(re, OUTPUT);
}

void drive_motors(int lpwm, char ldir, int rpwm, char rdir) {
  switch (ldir) {
    case 'f':
      digitalWrite(lf, HIGH);
      digitalWrite(lb, LOW);
      break;
    case 'b':
      digitalWrite(lf, LOW);
      digitalWrite(lb, HIGH);
      break;
  }
  analogWrite(le, lpwm);

  switch (rdir) {
    case 'f':
      digitalWrite(rf, HIGH);
      digitalWrite(rb, LOW);
      break;
    case 'b':
      digitalWrite(rf, LOW);
      digitalWrite(rb, HIGH);
      break;
  }
  analogWrite(re, rpwm);
}

String packet = "";
bool started = false;
void loop() {
  char character = ' ';
  if (Serial.available() > 0) {
    character = Serial.read();
    //Serial.println(character);
    if (character == 's') {
      started = true;
      //Serial.print("came to start");
      return;
    }
    else if (character == 'e') {
      started = false;
      packet="";
      //Serial.println("came to end");
      return;
    }
    if (started == true) {
      //Serial.print(" mp ");
      packet += character;
    }
  }
  
  if (packet.length() == 8) {
    char left_direction = packet[0];
    char right_direction = packet[4];
    int left_pwm = atoi(packet.substring(1,4).c_str());
    int right_pwm = atoi(packet.substring(5).c_str());
    drive_motors(left_pwm, left_direction, right_pwm, right_direction);
  }
}
