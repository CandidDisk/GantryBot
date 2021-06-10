from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import mathFunc
import time

class motor():
    def __init__(self):
        self.zeroDone = False
        self.startZero = False
        self.moveReady = False
        self.moveDone = False
        self.moveCount = 0

# This takes the digital dial reading & produces # of steps 
# for the clearCore during zeroing 

def formatMsg(dialRead):
    outMsg = "no"

    try:
        one = int(dialRead[6])
        tenth = int(dialRead[8])
        hundredth = int(dialRead[9])
        thousandth = int(dialRead[10])

        if (one == 2):
            if (tenth+hundredth+thousandth == 0):
                outMsg = "stp"
            else:
                outMsg = "1"
        else:
            if (one == 1):
                if (tenth > 7):

                    outMsg="-1"
                else:
                    outMsg = "-200"
            else:
                outMsg = "-1000"
        return outMsg
    except:
        return "no"

# serialDevices should be tuple of 3 devices, (clearCore, micro, laser)

# Handles zeroing process by reading digital dial & issuing instructions to clearCore
def runZero(motor, serialDevices, microZero=True):
    if microZero:
        clearCore = serialDevices[0]
    else:
        clearCore = serialDevices
    while not motor.startZero:
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
                        out = formatMsg(input)
                        clearCore.writeOut(out)
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
        if (serialDevices[0].readIn() == "move"):
            motor.moveReady = True
            motor.moveDone = False
    if (motor.moveReady):
        time.sleep(5)
        serialDevices[0].writeOut("move")
        serialDevices[0].writeOut(f"{stepsAdjusted}")
        motor.moveReady = False
    while (not motor.moveDone):
        if (serialDevices[0].readIn() == "moveDone"):
            print("move done")
            motor.moveDone = True

def runMoves(steps, amountOfSteps, motor, serialDevices, straightHome = True):
    # amountOfSteps+1 for returning back to zero in one move, 
    # amountOfSteps*2 for returning back to zero in same amount of moves & steps per move
    try:
        clearCore = serialDevices[0]
    except:
        clearCore = serialDevices
    if straightHome:
        stepsRange = amountOfSteps+1
        stepMulti = amountOfSteps*-1
    else:
        stepsRange = amountOfSteps*2
        stepMulti = -1

    for i in range(stepsRange):
        stepsAdjusted = steps
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*stepMulti)

        runOneMove(motor, clearCore, stepsAdjusted)

        mmDistance = mathFunc.calcDist(6400, stepsAdjusted)
        meterDistance = float(mmDistance / 1000)
        totalStep = float(mathFunc.calcDist(6400, steps * (i + 1))/1000)

        print(f"Total calcualted step distance = {totalStep}m")
        time.sleep(1)
    return True