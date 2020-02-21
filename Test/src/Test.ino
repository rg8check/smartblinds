/*
 * Project SmartBlinds
 * Description: Transfered arduino code
 * Author: Richard Sandvoss
 * Date:
 */


//Lets include some libaries
//#include <lowPower.h>
#include <math.h>

//Lets  create some variables
Servo myServo;
const byte NUM_BYTES = 2; //The BH1750 relays data in two bytes
byte buff[NUM_BYTES]; // creates an array to store data
int BH1750address = 0x23; // the address of the I2C device
int collectionNum = 0; // an indexing variable in a for loop. Data is collected 24 times between sleeps









// // setup() runs once, when the device is first turned on.
void setup() {
Serial.begin(57600);
Serial.println("initialising");
//delay(100); - probably not needed.
Wire.begin();

}

// loop() runs over and over again, as quickly as it can execute.
void loop() {
int iterNum = 24;
  if(collectionNum < iterNum){ // number of iterations before sleeping
    BH1750_Init(BH1750address); // initializes the I2C connection
    if(BH1750_Read(BH1750address) == NUM_BYTES){
        Serial.println("correct read count"); // checks if 2 values were read from the BH1750
    }
    /* 
     *  since val is an unsigned 16 bit integer, this next code will essential append buff[1] to the end of 
     *  buff[0]. It shifts buff[0] 8 bits left first. See datasheet for more information
     */
    float Nval = ((((buff[0]<<8)|buff[1])/1.2) - 5)*160/1000; 
    int mid = (int) Nval; // this just casts this to an int
    int fin; // The values fin is limited by will be determined by a calibration subroutine at the beginning of the program
    if(mid < 159){
      fin = mid;
    }
    else{
      fin = 159;
    }
    // writes values to servos and or steppers
    myServo.write(fin);
    sleep(); // gives a period of time betewen each adjustment
    collectionNum++;
  }
  
  else{ // sleeps after adjusting for a while
    for(int i = 0; i < 24; i++){
      sleep();
    }
  }
  collectionNum = 0; //resets the collection number
}
int* calibrate(int foo[2]) { // this pointer is needed to access the array. It may be necessary to pass foo as a parameter. I'm not sure. 

  return foo ; 
}
//meant to reduce power consumption and limit blind adjustments by "sleeping the photon for a period of time"
void sleep(){
  int lowPowerTime = 8; //number of seconds each sleep cycle lasts. 
  int totalTime = 1800; //total number of seconds for all sleep cycles.
  int totalCycles = totalTime/lowPowerTime;

  for(int i = 0; i < totalCycles; i ++){
    
    // LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); // TODO: download LowPower.h
   //This will sleep the ATMEGA microcontroller, Analog to digital converter, and Brownout detector
   //Works best on non-arduino boards
  }
}
//reads data from the BH1750. Typically returns 2. 
int BH1750_Read(int address){
   int byteNum = 0; //stores which bytes have been collected

  Wire.requestFrom(address,2); // collects two bytes from the BH1750
  while(Wire.available()){
    buff[byteNum] = Wire.read(); // receives one byte
    byteNum++;
  }

  return byteNum; // used to signal when two bytes have been read
}
// initializes the BH1750. I'll be honest - this is a black box
//Don't mess with this
void BH1750_Init(int address){
  Wire.beginTransmission(address); 
  Wire.write(0X10);
  Wire.endTransmission();
}