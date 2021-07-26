#include <Encoder.h>

#define baudRateSerial 9600

#define SerialPort Serial

const byte numChars = 64;

char receivedChars[numChars];

bool commHandShake(String check, bool sendCheck=true);

Encoder myEnc(4, 2);

void setup() {
  Serial.begin(9600);

  Serial.setTimeout(50);
}

long oldPosition  = -999;

void loop() {
    long newPosition = myEnc.read();
    if (newPosition != oldPosition) {
        oldPosition = newPosition;
        //Serial.println(newPosition);
    }
    if (commHandShake("zero", false)) {
        myEnc.write(0);
        Serial.println("zero");
    }
    if (commHandShake("read", false)) {
        Serial.println(newPosition);
    }
}

bool commHandShake(String check, bool sendCheck) {
    const char* checkStr = check.c_str(); 

    if (sendCheck) {
        Serial.println(check);
    }

    if (strcmp(readDataPi(), checkStr)==0) {
        return true;
    } else{
        return false;
    };
}

char* readDataPi(){
    static byte ndx = 0;
    char val;
    char endMarker = '\n';

    while (Serial.available() > 0) {
        val = Serial.read();

        if (val != endMarker) {
            receivedChars[ndx] = val;
            ndx++;
            if (ndx >= numChars) {
            ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            return receivedChars;
        }
    
    }
    
}
