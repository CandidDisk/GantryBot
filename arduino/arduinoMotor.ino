#include <Stepper.H>
#include <math.h>
#include <SpeedyStepper.h>

SpeedyStepper stepperX;
SpeedyStepper stepperY;

void setup() {
    Serial.begin(9400);
    int outputs[] = {13, 12, 11, 10, 9, 8, 6, 5, 4, 3, 2};

    for (int i : outputs) {
        pinMode(i, OUTPUT);
    }
    pinMode(A1, OUTPUT);

    pinMode(A3, INPUT);
    pinMode(A0, INPUT);

    pinMode(A4, INPUT);
    pinMode(A5, INPUT);

}

void motorEnable(int hi, int lo) {
    digitalWrite(hi, HIGH);
    digitalWrite(lo, LOW);
}