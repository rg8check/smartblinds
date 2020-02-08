#include <LowPower.h>
#include <Wire.h> //BH1750 IIC Mode 
#include <math.h> 
#include <Servo.h>

int BH1750address = 0x23; //setting i2c address
Servo myservo;
Servo myservo1;
byte buff[2];
int q = 0;

void sleep(){
  int tim1 = 1800/8;
  for (int i = 0; i < tim1; i++)
  {
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
    }
}
void setup() {
  Serial.begin(57600);
  Serial.println("Initialising...");
  delay(100);
  Wire.begin();
  myservo.attach(4);
  myservo1.attach(5);
  myservo.write(90);// set servo to start
  myservo1.write(90);
  Serial.println("Initialisation complete.");
  delay(100);
}

void loop() {
if(q < 24){
int i;
uint16_t val=0;
BH1750_Init(BH1750address);

  if(2==BH1750_Read(BH1750address))
  {
    
    val=((buff[0]<<8)|buff[1])/1.2;
    val=val+15;
  }
    float Nval = ((((buff[0]<<8)|buff[1])/1.2) - 5)*160/1000;
    int mid = (int) Nval;
    float fin;
    if(mid < 159){
     fin = mid;}
    else{
      fin = 159;
      }
    Serial.print(fin,DEC);
    myservo.write(fin);
    myservo1.write(fin);
    Serial.print("     ");
    Serial.print((((buff[0]<<8)|buff[1])/1.2));
    Serial.print("     ");
    Serial.println(q);
    delay(1000);
q++;
sleep();
}
else{
 for(int z = 0; z < 24; z++){
    Serial.print("Sleep");
    Serial.println(z);
    delay(100);
    sleep();
  }
 q = 0;
}
}

int BH1750_Read(int address) //
{
  int i=0;

  //Serial.println(F("Read function: "));   // added
  
  Wire.requestFrom(address, 2);
  while(Wire.available()) //
  {
    buff[i] = Wire.read();  // receive one byte

   // Serial.print(buff[i], DEC);   // added
   // Serial.print(F(", "));   // added

    i++;
  }
 // Serial.println();

  return i;
}
void BH1750_Init(int address) 
{
  Wire.beginTransmission(address);
  Wire.write(0x10);//1lx reolution 120ms
  Wire.endTransmission();
}
