#include <SpeedyStepper.h>
#include <AccelStepper.h>

#define CLOCK_PIN A1
#define DATA_PIN A0
#define SENSOR_DIG 2

AccelStepepr stepper = AccelStepper(AccelStepper::FULL2WIRE, 10, 11);


SpeedyStepper stepper;

long proxPos;
long zeroPos;

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

    /*stepper.connectToPins(11, 10);

    stepper.setSpeedInStepsPerSecond(100000);
    stepper.setAccelerationInStepsPerSecondPerSecond(1000);*/

    stepper.setMaxSpeed(500);
    stepper.setAcceleration(300);

    
    while (digitalRead(SENSOR_DIG) == LOW){
        stepper.move(-10000);
        while(stepper.currentPosition() != -10000){

            if (digitalRead(SENSOR_DIG) == HIGH){
                Serial.println("Proximity sensor tripped(0)");
                proxPos = stepper.currentPosition();
                Serial.print("Proximity absolute position = ");Serial.print(proxPos);Serial.print(" steps");
                stepper.stop();
            }
            stepper.run();
        }
    }
    stepper.setMaxSpeed(100);
    stepper.setAcceleration(100);
}

unsigned long tmpTime;
long value;
float result;
int i = 0;

void loop() {

    if (digitalRead(SENSOR_DIG) == HIGH){
        
        while(digitalRead(CLOCK_PIN)==LOW){}
        tmpTime=micros();
        while(digitalRead(CLOCK_PIN)==HIGH){}

        if((micros()-tmpTime)<500) return;

        readMicrometer();

        if (result==8192){
            stepper.stop();
            zeroPos = stepper.currentPosition();
            Serial.println("Currently zeroed");
        } else {
            if (result > 6000){
                if (result < 7000){
                    stepper.move(-10);
                } else if (result < 8193){
                    delay(100);
                    stepper.move(-1);
                }
                if (result > 8192){
                    delay(100);
                    stepper.move(1);
                }
                if (result==6544 || result==6512){
                    stepper.move(1);
                    Serial.println("6544 i just moved 1");
                    delay(3000);
                }
            } else {stepper.move(-50);}
            stepper.run(); 
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
    Serial.println(value);
    result = value;

}

void motorEnable(int hi, int lo) {
    digitalWrite(hi, HIGH);
    digitalWrite(lo, LOW);
}
