//#include <LowPower.h>
#include <Wire.h> //BH1750 IIC Mode 
#include <math.h> 
#include <Servo.h> // Up to 12 servos can be supported on an arduino. 

int BH1750address = 0x23; //setting i2c address: do not change; this is what the arduino code will look for when it tries to connect over I2C
Servo myservo;
Servo myservo1; // likely a change made to allow the arduino to control multiple servos. If powering more than 1, must use an external power supply.
const byte TO_READ = 2; //Data is output in two bytes
byte buff[TO_READ]; // creates a byte array of size TO_Read that will hold data from the BH1750
int q = 0; //TODO: figure out what this is.

void sleep(){//reduces power consumption of arduino while not in use
  int lowPowerTime = 8; // the amount of time the arduino sleeps each time lowPower.powerDown is called
  int totalTime = 1800; // the total amount of time the arduino will sleep when this is called in seconds (30 min)
  int tim1 = totalTime/lowPowerTime;
  for (int i = 0; i < tim1; i++)
  {
   // LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); // TODO: download LowPower.h
   //This will sleep the ATMEGA microcontroller, Analog to digital converter, and Brownout detector
   //Works best on non-arduino boards
   
    }
}
void setup() {
  Serial.begin(57600); // begins serial communication at 57600 baud rate
  Serial.println("Initialising...");// good for troubleshooting
  delay(100); // is this necessary?
  Wire.begin(); // begins communication over I2C with the BH1750
  myservo.attach(4); // the first servo motor attaches to pin 4
  myservo1.attach(5);
  myservo.write(90);// set servo to start -this is the initial angle in degrees. If a continuous rotation servo, this would mean no rotation.
  myservo1.write(90);
  Serial.println("Initialisation complete.");
  delay(100);
}

void loop() {
if(q < 24){ // Second use of q?
//int i; // what is this?
uint16_t val=0; //tores the appended values of buff[0] and buff[1]
BH1750_Init(BH1750address); //Initializes the I2C connection at this address

  if(2==BH1750_Read(BH1750address))
  {
    /* 
     *  since val is an unsigned 16 bit integer, this next code will essential append buff[1] to the end of 
     *  buff[0]. It shifts buff[0] 8 bits left first. I have no clue why it is divided by 2 and then increased by 15.
     */
    val=((buff[0]<<8)|buff[1])/1.2;
    val=val+15;
  }
  
    float Nval = ((((buff[0]<<8)|buff[1])/1.2) - 5)*160/1000; 
    int mid = (int) Nval;
    float fin;
    //The  next part of the code limits fin to between o and 159 degrees.
    //This is what our calibration program would replace.
    if(mid < 159){
     fin = mid;}
    else{
      fin = 159;
      }
    Serial.print(fin,DEC); // prints fin in base 10. Why?
    myservo.write(fin); // ok. So fin is the angle it rotates to. 
    myservo1.write(fin); // rotates both servos to fin degrees
    Serial.print("     ");
    Serial.print((((buff[0]<<8)|buff[1])/1.2)); 
    Serial.print("     ");
    Serial.println(q); 
    delay(1000); // delays 1 second
q++; 
sleep(); //after adjusting 24 times, it goes to sleep for 30 minutes?
q=0;
}
else{ // does this else correspond with the first or second if statement?
 for(int z = 0; z < 24; z++){
    Serial.print("Sleep");
    Serial.println(z);
    delay(100);
    sleep(); // sleeps it for 12 hours?
  }
 q = 0;
}
}

int BH1750_Read(int address) //most likely example code. Will get data from light sensor.
{
  int i=0;

  //Serial.println(F("Read function: "));   // added
  
  Wire.requestFrom(address, 2);
  while(Wire.available()) //
  {
    buff[i] = Wire.read();  // receive one byte

    Serial.print(buff[i], DEC);   // added
    Serial.print(F(", "));   // added

    i++;
  }
 // Serial.println();

  return i;
}
void BH1750_Init(int address) 
{
  Wire.beginTransmission(address);
  Wire.write(0x10);//1lx reolution 120ms what does this do?
  Wire.endTransmission();
}
