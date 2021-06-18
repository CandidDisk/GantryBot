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

bool receiveStp = false;

bool newData = false;

bool zeroDone = true;

bool setupDone = false;

bool moveReady = true;

bool moveDistance(int32_t distance);

bool moveAtVelocity(int32_t velocity);

bool MoveAbsolutePosition(int32_t position);

bool commHandShake(String check, bool sendCheck=true);


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

    // Wait until pi-clearCore handshake is complete
    while (true) {
        if (strcmp(readDataPi(),"start")==0) {
            zeroDone = false;
            break;
        } else {Serial.println("start");}
        delay(100);

    }

    // Wait until motor is ready
    while (motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {continue;}

    // Move if magnetic is not triggered
    if (digitalRead(SENSOR_DIG) == HIGH) {moveAtVelocity(-10000);}

    while (digitalRead(SENSOR_DIG) == HIGH) {}

    if (digitalRead(SENSOR_DIG) == LOW) {
        moveAtVelocity(0);
    }

    velocityLimit = 500000;

    accelerationLimit = 10000;
}

void loop() {
    moveReady = false;
    delay(2000);
    moveTest();
}

void moveTest() {

    while (!moveReady) {

        if (commHandShake("move")) { 
            int stepsToMove = 0;
            while (stepsToMove == 0){
                String stepsToMoveStr = readDataPi();
                stepsToMove = stepsToMoveStr.toInt();

                delay(10);
                if (stepsToMove != 0){
                    break;  
                }
            }
            moveDistance(stepsToMove);
            stepsToMove = 0;
            moveReady = false;
            Serial.println("moveDone");
            break;
        }
        delay(10);
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


// build char* array out of pi output 
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
    } else if (strcmp(received, "stpFinal")== 0){
        motor.MoveStopAbrupt();
        moveAtVelocity(0);
        zeroDone = true;
    } else {
        int stepsToMove = 0;
        while (stepsToMove == 0){
            String stepsToMoveStr = readDataPi();
            stepsToMove = stepsToMoveStr.toInt();
            delay(5);
            if(stepsToMove != 0){
                break;
            }
        }
        if (stepsToMove < -10) {
            moveAtVelocity(stepsToMove);
        } else {
            moveDistance(stepsToMove);
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
