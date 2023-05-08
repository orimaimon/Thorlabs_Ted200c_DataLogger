
#include <Wire.h>
#include <Adafruit_MCP4725.h>
#include <Adafruit_ADS1X15.h>


Adafruit_ADS1115 ads;
Adafruit_MCP4725 dac;
double Vin;
double dataIn = 0;

const float multiplier = 2*0.1875F;
// Set this value to 9, 8, 7, 6 or 5 to adjust the resolution
#define DAC_RESOLUTION    (9)

void setup(void) {

  Serial.begin(9600);
  ads.begin(0x48);
  ads.setGain(GAIN_TWOTHIRDS);
  dac.begin(0x60); //I have my ADDR pin connected to GND so address is 0x60
  dac.setVoltage((dataIn*4095)/10, false);
}

void loop(void) {
  if (Serial.available())
    {
        String fromGUI = Serial.readString();

       
        dataIn = fromGUI.toDouble();
        dac.setVoltage(dataIn, false);
    }      
 int16_t adc0;

 adc0 = ads.readADC_SingleEnded(3);
 Vin = adc0 * multiplier;
 Serial.println(Vin);
 

 delay(1000);

}
