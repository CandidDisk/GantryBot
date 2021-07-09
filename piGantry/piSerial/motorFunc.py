from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import mathFunc
import time

class motor():
    def __init__(self):
        self.zeroDone = False
        self.startZero = False
        self.moveReady = False
        self.moveDone = False
        self.middleDone = False
        self.moveCount = 0
        self.middleOffset = int(0)
        self.maxTravel = int(0)
        self.startOffset = int(0)
        self.endOffset = int(0)
        self.pulsePerRev = int(12800)

# This takes the digital dial reading & produces # of steps 
# for the clearCore during zeroing 

def formatMsg(dialRead, target):
    outMsg = "no"

    if (dialRead == target):
        outMsg = "stp"
    if (dialRead > target):
        outMsg = "1"
    if (dialRead < target):
        if (dialRead > (target/1.2)):
            print(dialRead)
            print((target/1.2))
            outMsg = "-1"
        else:
            outMsg = "-200"
    return outMsg

# serialDevices should be tuple of 3 devices, (clearCore, micro, laser)

# Handles zeroing process by reading digital dial & issuing instructions to clearCore
def runZero(motor, serialDevices, zeroPoint, microZero=True):
    if (type(serialDevices) is tuple):
        clearCore = serialDevices[0]
    else:
        clearCore = serialDevices
    while not motor.startZero :
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            if microZero:
                stpCount = 0
                while (clearCore.readIn() != "zero"):
                    if (clearCore.readIn() == "zero"):
                        break
                while not motor.zeroDone:
                    # If "stp" command issued 50 times, read clearCore output for "done" msg
                    if (stpCount > 50):
                        motor.zeroDone = True
                        clearCore.writeOut("stpFinal")
                        break
                    else:
                        # Call on readDial function passing micro.port initialized in class constructor
                        input = serialComm.readDial(serialDevices[1].port)
                        out = formatMsg(input, zeroPoint)
                        clearCore.writeOut(out)
                        print(out)
                        if (out == "stp"):
                            stpCount += 1
                        else:
                            stpCount = 0
    if microZero:
        clearCore.writeOut("done")

# Handles running a set of moves w/ same amount of steps per move
# Issues clearCore steps to move after taking a reading 

# 128000, 31 almost full travel 4.8 meters | 819200, 4 3.84 meters
# 128000, 20 3 meters | 1280000, 1 1.5 meters

def runOneMove(motor, clearCore, stepsAdjusted):
    while (not motor.moveReady):
        if (clearCore.readIn() == "move"):
            motor.moveReady = True 
            motor.moveDone = False
    if (motor.moveReady):
        time.sleep(0.1)
        clearCore.writeOut("move")
        clearCore.writeOut(f"{stepsAdjusted}")
        motor.moveReady = False
    while (not motor.moveDone):
        if (clearCore.readIn() == "moveDone"):
            print("move done")
            motor.moveDone = True

def adjustToEncoder(clearCore, encoder, meterDistance):
    while (serialComm.readArduinoEncoder(encoder) != meterDistance):
        encoderReading = serialComm.readArduinoEncoder(encoder)
        print(encoderReading)
        diff = encoderReading - meterDistance
        if (serialComm.readArduinoEncoder(encoder) < meterDistance):
            runOneMove(motor, clearCore, 10)
        elif (serialComm.readArduinoEncoder(encoder) > meterDistance):
            runOneMove(motor, clearCore, -10)

def runMoves(steps1, motorObj, serialDevices, steps2 = False, straightHome = True, encoder = False, jiggle = False):
    # amountOfSteps+1 for returning back to zero in one move, 
    # amountOfSteps*2 for returning back to zero in same amount of moves & steps per move
    print(f"{type(motorObj)} yo")
    wiggleHome = False
    if (type(serialDevices) is tuple):
        clearCore = serialDevices[0]
        clearCore2 = serialDevices[1]
    else:
        clearCore = serialDevices
    if (type(motorObj) is tuple):
        print(f"{type(motorObj)} yo2")
        motor = motorObj[0]
        print(f"{type(motorObj)} yo3")
        motor2 = motorObj[1]
    else:
        motor = motorObj
        
    amountOfSteps = steps1[1]
    steps = steps1[0]
    if straightHome:
        stepsRange = amountOfSteps+1
        stepMulti = amountOfSteps*-1
    else:
        stepsRange = amountOfSteps*2
        stepMulti = -1

    if (type(encoder) is tuple):
        encoderReader = encoder[1]

    for i in range(stepsRange):
        stepsAdjusted = steps
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*stepMulti)
            if not wiggleHome:
                for i in range(2):
                    runOneMove(motor, clearCore, 200)
                    runOneMove(motor, clearCore, -200)
                wiggleHome = True
            print("Going home")
            print(serialComm.readArduinoEncoder(encoderReader))
            foo = input("Press Enter to continue...")
            #time.sleep(15)

        mmDistance = mathFunc.calcDist(12800, stepsAdjusted)
        meterDistance = float(mmDistance / 1000)
        totalStep = float(mathFunc.calcDist(12800, steps * (i + 1))/1000)

        print(f"Total calcualted step distance = {totalStep}m")
        if steps2:
            runMoves(steps2, motor2, clearCore2)
        runOneMove(motor, clearCore, stepsAdjusted)
        if encoder:
            if encoder[0]:
                adjustToEncoder(clearCore, encoder[1], meterDistance)
        if jiggle:
            for i in range(2):
                runOneMove(motor, clearCore, 200)
                runOneMove(motor, clearCore, -200)
        if encoder:
            print(serialComm.readArduinoEncoder(encoder[1]))
        #print("Take reading!")
        #time.sleep(15)
    return True