#include "ClearCore.h"

#define motor ConnectorM0

#define baudRateSerial 1000000

#define SerialPort Serial

#define SENSOR_DIG IO4

int velocityLimit = 10000;
int accelerationLimit = 100000;

bool MoveDistance(int distance);

const byte numChars = 64;

char receivedChars[numChars];

bool newData = false;

bool moveAtVelocity(int32_t velocity);

bool zeroDone = false;

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

}

void loop() {
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
            //newData = true;
        }
    }
    /*if (newData == true) {
        Serial.print(receivedChars);
        newData = false;
    }*/
    
    if (strcmp(receivedChars,"stp")==0) {
        motor.MoveStopAbrupt();
        moveAtVelocity(0);
        zeroDone = true;
    } else {
        if (strcmp(receivedChars,"m0-")==0) {
            moveAtVelocity(-1000);
        }
        if (strcmp(receivedChars,"s1-")==0) {
            moveAtVelocity(-200);
        }
        if (strcmp(receivedChars,"s2-")==0) {
            moveDistance(-5);
            delay(50);
        }
        if (strcmp(receivedChars,"s0+")==0) {
            moveDistance(5);
            delay(50);
        }
    }
    /*
    while (Serial.available() > 0) {

        val = val + (char)Serial.read(); 
        
        //val = Serial.readString();
    }

    Serial.print(val);
    if (val.equals("m0-\n")) {
        Serial.print("Yes!");
    } else {
        Serial.print(val);
    }
    Serial.print(val.equals("m0-\n")); */

    
    /*if (val == "stp\n") {
        motor.MoveStopAbrupt();
        moveAtVelocity(0);
    } else {
        if (val == "m0-\n") {
            moveAtVelocity(-5000);
        }
        if (val == "s1-\n") {
            moveAtVelocity(-1000);
        }
        if (val == "s2-\n") {
            moveAtVelocity(-10);
        }
        if (val == "s0+\n") {
            moveAtVelocity(100);
       d }
    }*/

}
bool MoveDistance(int distance) {
    // Check if an alert is currently preventing motion
    if (motor.StatusReg().bit.AlertsPresent) {
        Serial.println("Motor status: 'In Alert'. Move Canceled.");
        return false;
    }

    Serial.print("Moving distance: ");
    Serial.println(distance);

    // Command the move of incremental distance
    motor.Move(distance);

    // Waits for HLFB to assert (signaling the move has successfully completed)
    Serial.println("Moving.. Waiting for HLFB");
    while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }

    Serial.println("Move Done");
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
        Serial.println("Motor status: 'In Alert'. Move Canceled.");
        return false;
    }

    Serial.print("Moving to absolute position: ");
    Serial.println(position);

    // Command the move of absolute distance
    motor.Move(position, MotorDriver::MOVE_TARGET_ABSOLUTE);

    // Waits for HLFB to assert (signaling the move has successfully completed)
    Serial.println("Moving.. Waiting for HLFB");
    while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
        continue;
    }

    Serial.println("Move Done");
    return true;
}
/*
bool moveDistanceToMag(int velocity) {
    // Check if an alert is currently preventing motion
    if (motor.StatusReg().bit.AlertsPresent) {
        return false;
    }



    //SerialPort.print("<Moving velocity: >");
    //SerialPort.println(velocity);

    if (digitalRead(SENSOR_DIG) == LOW){
        SerialPort.println(digitalRead(SENSOR_DIG));
        //motor.MoveStopAbrupt();
        return true;
    } else {
        //motor.MoveVelocity(velocity);

        // Waits for HLFB to assert (signaling the move has successfully completed)
        while (!motor.StepsComplete() || motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
            if (digitalRead(SENSOR_DIG) == LOW){
                //motor.MoveStopAbrupt();
                return true;
                break;
            } else {continue;}
        }
    }
    // Command the move of incremental distance



    return true;
}
*/


