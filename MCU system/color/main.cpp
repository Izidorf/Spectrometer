#include "mbed.h"
#include "USBSerial.h"

Serial pc(USBTX, USBRX); // tx, rx

//Color Sensor
AnalogIn bluepin(p20);    
AnalogIn greenpin(p19);
AnalogIn redpin(p18);

PwmOut grd(p21);    // another ground PIN
PwmOut led(p26);   // 

double blue = 0.0;
double green = 0.0;
double red= 0.0;
double color[3];

//Luminosity Light
PwmOut lumlightPW(p24);
PwmOut lumlightGRD(p23);

//IR sensor
AnalogIn irpin(p17);    
PwmOut irgrd(p22);    // another ground PIN
PwmOut irpower(p25);
float irData=0;


double map(double x, double in_min,double in_max, double out_min, double out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

double * measureColor(int N, int ledOn){
    led = ledOn;
    wait(0.5);
    
    //Read the values from the sensor
    int i=0;
    for(i=0; i<N; i++){
        red += redpin.read();
        green += bluepin.read();
        blue += greenpin.read();
    }    
    
    red /= N;
    green /= N;
    blue /= N; 
    
    red =   ( red    * 100.0); // / 16.0);
    green = ( green  * 130.0 ); /// 22.0);
    blue =  ( blue   * 200.0 ); /// 25.0); 

    
    
    led = 0; //turn of led
    color[0] = red;
    color[1] = green;
    color[2] = blue;
    
    return color;
}

double  measureLuminance(int N){
    lumlightPW = 1;
    
    wait(1);
    //Read the values from the sensor
    int i=0;
    for(i=0; i<N; i++){
        red += redpin.read();
        green += bluepin.read();
        blue += greenpin.read();
    }    
    
    red /= N;
    green /= N;
    blue /= N; 
        
    lumlightPW = 0;
        
    return (0.2126 *red  + 0.7152 *green + 0.0722 *blue);    
}

double measureIR(int N){
    int i=0;
    for(i=0; i<N; i++){
        irData += irpin.read();
    }    
    
    return irData/=N;
}

void printCSV(double *rgb, double lum, double ir){
    pc.printf("%f,%f,%f,%f,%f \n", *(rgb+0),*(rgb+1),*(rgb+2), lum, ir);
}

void setup(){
    grd=0;
    
    //Color sensor
    double *rgb = measureColor(50,1);
    
    pc.printf("\nRGB values\n");
    pc.printf("Red: ");
    pc.printf("%f ", *(rgb+0));
    pc.printf("Green: ");
    pc.printf("%f ", *(rgb+1));
    pc.printf("Blue:");
    pc.printf("%f \n\r", *(rgb+2));
   
    //Calculate Luminance
    double lum = measureLuminance(50);
    pc.printf("Luminance:\n val: %f \n\r", lum);
    
    //IR sensor
    double irData = measureIR(50);
    pc.printf("IR: \n val: %f \n\r", irData);  
    
    pc.printf("Red,Green,Blue,Lum,IR\n");  
}

int main() {
  

 
  setup();
 
  while(1){   
    //Color sensor
    double *rgb = measureColor(50,1);
    
    //Calculate Luminance
    double lum = measureLuminance(50);
 
    //IR sensor
    double irData = measureIR(50);
   
    printCSV(rgb, lum, irData);
    
    wait(1);      
  }
}