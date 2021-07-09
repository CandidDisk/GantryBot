#define baudRateSerial 9600
#define SerialPort Serial

// pins for the encoder inputs
#define RH_ENCODER_AP 2 
#define RH_ENCODER_BP 4
#define RH_ENCODER_AN 3 
#define RH_ENCODER_BN 5

// variables to store the number of encoder pulses
volatile long rightCountN = 0;
volatile unsigned long totalCount = 0;


const byte numChars = 64;

char receivedChars[numChars];

char inputData[numChars];

bool newData = false;

void setup() {
    Serial.begin(baudRateSerial);

    Serial.setTimeout(50);

    // Wait until pi-clearCore handshake is complete
    while (true) {
        if (strcmp(readDataPi(),"start")==0) {
            break;
        } else {Serial.println("start");}
        delay(100);
    }
    pinMode(RH_ENCODER_AP, INPUT);
    pinMode(RH_ENCODER_BP, INPUT);
    pinMode(RH_ENCODER_AN, INPUT);
    pinMode(RH_ENCODER_BN, INPUT);
    // initialize hardware interrupts
    attachInterrupt(1, rightEncoderEventN, CHANGE);
    
}

void loop() {
    Serial.println(rightCountN);
    delay(150);
}

void rightEncoderEventN() {
    if (digitalRead(RH_ENCODER_AN) == HIGH) {
        if (digitalRead(RH_ENCODER_BN) == LOW) {
        rightCountN--;
        } else {
        rightCountN++;
        }
    } else {
        if (digitalRead(RH_ENCODER_BN) == LOW) {
        rightCountN++;
        } else {
        rightCountN--;
        }
    }
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
            newData = true;
            return receivedChars;
        }
    
    }
    
}

// Send msg to pi & wait until pi returns same msg
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
    delay(10);
}
