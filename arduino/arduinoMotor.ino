#include <Stepper.H>
#include <math.h>
#include <SpeedyStepper.h>

SpeedyStepper stepperX;
SpeedyStepper stepperY;

const byte numChars = 64;
char receivedChars[numChars];

void setup() {
    Serial.begin(9400);

    pinMode(LED_BUILTIN, OUTPUT);

    ledExpressStatus(LED_BUILTIN, 200);

    Serial.println("<Arduino ready>");

    int outputs[] = {13, 12, 11, 10, 9, 8, 6, 5, 4, 3, 2};

    for (int i : outputs) {
        pinMode(i, OUTPUT);
    }
    pinMode(A1, OUTPUT);

    pinMode(A3, INPUT);
    pinMode(A0, INPUT);

    pinMode(A4, INPUT);
    pinMode(A5, INPUT);

    ledExpressStatus(LED_BUILTIN, 200);

    Serial.println("<Servomotors ready>");

}

void moveToPoints(){
      
}

void motorEnable(int hi, int lo) {
    digitalWrite(hi, HIGH);
    digitalWrite(lo, LOW);
}

void ledExpressStatus(pin, delay){
    digitalWrite(pin, HIGH);
    delay(delay);
    digitalWrite(pin, LOW);
    delay(delay);
    digitalWrite(pin, HIGH);
}