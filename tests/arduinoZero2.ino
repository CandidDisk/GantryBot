#include <SpeedyStepper.h>

#define CLOCK_PIN A1
#define DATA_PIN A0
#define SENSOR_DIG 2

SpeedyStepper stepper;

void setup(){
    Serial.begin(4800);

    pinMode(CLOCK_PIN, INPUT);
    pinMode(DATA_PIN, INPUT);
    pinMode(SENSOR_DIG, INPUT);


    int output[] = {13, 12, 11, 10, 9, 6};

    /*
        Input A+ = ~10 | Input A- = ~9
        Input B+ = ~11 | Input B- = ~6
        Enable + = 7 | Enable - = 12
    */
    for (int i : output) {
        pinMode(i, OUTPUT);
    }
    pinMode(5, INPUT); //HLFB-
    pinMode(3, INPUT); //HLFB+

    //Turning motor on
    motorEnable(13, 12);
    stepper.connectToPins(11, 10);

    stepper.setSpeedInStepsPerSecond(1000);
    stepper.setAccelerationInStepsPerSecondPerSecond(100);

}

unsigned long tmpTime;
long value;
float result;

void loop() {
    if (digitalRead(SENSOR_DIG) == HIGH){
        
        while(digitalRead(CLOCK_PIN)==LOW){}
        tmpTime=micros();
        while(digitalRead(CLOCK_PIN)==HIGH){}

        if((micros()-tmpTime)<500) return;

        readMicrometer();
        //buf[0]=' ';
        //dtostrf(result*2.54,6,3,buf+1); strcat(buf," cm "); 
        Serial.print(result);
        if (result==81928192){
            //Turning motor off
            motorEnable(12, 7);
            Serial.println("Motor X is zeroed!");
        } else {

        }
    }
}

//65126512.00

void readMicrometer(){
    value = 0;
    for (int i=0; i<29; i++) {
        //Serial.print(digitalRead(DATA_PIN));
        while(digitalRead(CLOCK_PIN)==LOW){}
        while(digitalRead(CLOCK_PIN)==HIGH){}
        if(digitalRead(DATA_PIN)==HIGH){
            if(i<20) value|=(1<<i);
        }
    }
    Serial.print(value);
    result = value;

}

void motorEnable(int hi, int lo) {
  digitalWrite(hi, HIGH);
  digitalWrite(lo, LOW);
}