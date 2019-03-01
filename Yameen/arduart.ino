void setup()
{
  Serial.begin(9600);
}
long n = 1;
int j=1;
void loop()
{if (Serial.available()>0){
 char i = Serial.read();
 if (n%3==0){
   //Serial.print(j);
 //Serial.print('=');
 Serial.println(i);
 n=0;
 }
 else if(n%3!=0){
 //Serial.print(j);
 //Serial.print('=');
   Serial.print(i);
 }n++;
 j++;
 //Serial.print('\n');
 //Serial.print("n=");
 //Serial.println(n);
 }
}
