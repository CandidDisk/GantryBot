#include "ClearCore.h"

#define motor ConnectorM0

#define baudRateSerial 1000000

#define SerialPort Serial

#define SENSOR_DIG IO4

int velocityLimit = 10000;

int accelerationLimit = 100000;

const byte numChars = 64;

char receivedChars[numChars];

char inputData[numChars];

int tempVal = 0;

bool newData = false;

bool zeroDone = true;

bool setupDone = false;

bool moveReady = true;

bool moveDistance(int32_t distance);

bool moveAtVelocity(int32_t velocity);

bool MoveAbsolutePosition(int32_t position);


void setup() {
    SerialPort.begin(baudRateSerial); 

    pinMode(SENSOR_DIG, INPUT);

    MotorMgr.MotorInputClocking(MotorManager::CLOCK_RATE_NORMAL);

    MotorMgr.MotorModeSet(MotorManager::MOTOR_ALL,
                            Connector::CPM_MODE_STEP_AND_DIR);

    motor.HlfbMode(MotorDriver::HLFB_MODE_HAS_BIPOLAR_PWM);

    motor.HlfbCarrier(MotorDriver::HLFB_CARRIER_482_HZ);

    motor.VelMax(velocityLimit);

    motor.AccelMax(accelerationLimit);

    motor.EnableRequest(true);

    Serial.setTimeout(50);

    newData = true;

    while (true) {
        if (strcmp(readDataPi(),"start")==0) {
            zeroDone = false;
            break;
        } else {
            Serial.println("start");}
        
        delay(100);
        /*
        if (newData) {
            Serial.println("start");
            newData = false;
        }
        if (!newData) {
            if (strcmp(readDataPi(),"start")==0) {
                newData = true;
                zeroDone = false;
                break;
            } else {newData = false;}
        }*/

    }

    while (motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }

    if (digitalRead(SENSOR_DIG) == HIGH){
        moveAtVelocity(-10000);
    }

    while (digitalRead(SENSOR_DIG) == HIGH) {
        
    }

    if (digitalRead(SENSOR_DIG) == LOW) {
        moveAtVelocity(0);
    }



    while (!zeroDone) {
        zeroMotor(readDataPi());
        if (tempVal > 50) {
            zeroDone = true;
        }
    }
    newData = true;

    while (!setupDone) {
        if (commHandShake("done")) {
            setupDone = true;
        }

    }
}

void loop() {
    moveReady = false;
    delay(2000);
    moveTest();
}

void moveTest() {

    while (strcmp(readDataPi(), "move1")==1) {
        Serial.println("move1");
        delay(50);
    }
    if (strcmp(readDataPi(), "move1")==0) {
        moveReady = true;
        moveDistance(640000);
        moveReady = false;
    }

    while (strcmp(readDataPi(), "move1z")==1) {
        Serial.println("move1z");
        delay(50);
    }
    if (strcmp(readDataPi(), "move1z")==0) {
        moveReady = true;
        moveDistance(-640000);
        moveReady = false;
    }

    while (strcmp(readDataPi(), "move2")==0) {
        Serial.println("move2");
        delay(50);
    }
    if (strcmp(readDataPi(), "move2")==0) {
        moveReady = true;
        moveDistance(2560000);
        moveReady = false;
    }
    
    while (strcmp(readDataPi(), "move2z")==0) {
        Serial.println("move2z");
        delay(50);
    }
    if (strcmp(readDataPi(), "move2z")==0) {
        moveReady = true;
        moveDistance(2560000);
        moveReady = false;
    }
}

bool commHandShake(String check) {
    const char* checkStr = check.c_str(); 
    if (newData) {
        Serial.println(check);
        newData = false;
    } else {
        if (strcmp(readDataPi(), checkStr)==0) {
            newData = true;
            return true;
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

void zeroMotor(char* received){
    if (strcmp(received,"stp")==0) {
        motor.MoveStopAbrupt();
        moveAtVelocity(0);
        tempVal++;
    } else {
        if (strcmp(received,"m0-")==0) {
            moveAtVelocity(-1000);
        }
        if (strcmp(received,"s1-")==0) {
            moveAtVelocity(-200);
        }
        if (strcmp(received,"s2-")==0) {
            moveDistance(-1);
            delay(50);
        }
        if (strcmp(received,"s0+")==0) {
            moveDistance(1);
            delay(50);
        }
    }
}

bool moveDistance(int distance) {
    // Check if an alert is currently preventing motion
    if (motor.StatusReg().bit.AlertsPresent) {
        return false;
    }

    // Command the move of incremental distance
    motor.Move(distance);

    // Waits for HLFB to assert (signaling the move has successfully completed)
    while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }

    return true;
}

bool moveAtVelocity(int velocity) {
    if (motor.StatusReg().bit.AlertsPresent) {
        return false;
    }

    motor.MoveVelocity(velocity);

    while(!motor.StatusReg().bit.AtTargetVelocity) {
        continue;
    }

    return true;
}

bool MoveAbsolutePosition(int position) {
    // Check if an alert is currently preventing motion
    if (motor.StatusReg().bit.AlertsPresent) {
        return false;
    }



    // Command the move of absolute distance
    motor.Move(position, MotorDriver::MOVE_TARGET_ABSOLUTE);

    // Waits for HLFB to assert (signaling the move has successfully completed)
    while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }

    return true;
}
