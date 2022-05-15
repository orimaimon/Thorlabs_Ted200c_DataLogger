#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads;
const float multiplier = 2*0.1875F;
double Vin;
int digValue = 1;
int analogPin = 3;  
int dataIn = 1;
                   
 


void setup(){
   TCCR2B = TCCR2B & B11111000 | B00000011;
   pinMode(3,OUTPUT);
   Serial.begin(9600); //BaudRate
    ads.begin();
    analogWrite(analogPin, digValue);
    
   
}
void loop(){



if (Serial.available())
    {
        String fromGUI = Serial.readString();

       
        dataIn = fromGUI.toInt();
    }

       

        
 int16_t adc0, adc1, adc2, adc3;
 
  
  adc0 = ads.readADC_SingleEnded(0);
  adc1 = ads.readADC_SingleEnded(1);
  adc2 = ads.readADC_SingleEnded(2);
  adc3 = ads.readADC_SingleEnded(3);
  Vin = adc0 * multiplier;
   /* Serial.print("AIN: "); Serial.println(adc0 * multiplier);*/
      Serial.println(Vin);
   
if (0<=dataIn && dataIn<=255) {

     analogWrite(analogPin, dataIn);
      } 

  

   
delay(1000); //for maintaining the speed of the output in serial moniter
}
