void setup()
{
  Serial.begin(115200);
}
void loop()
{if (Serial.available()>0){
 char i = Serial.read();
 Serial.println(i);
 Serial.print('\n');}
}
