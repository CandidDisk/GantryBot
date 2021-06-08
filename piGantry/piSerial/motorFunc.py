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
def runZero(motor, serialDevices):
    while not motor.startZero:
        if (serialDevices[0].readIn() == "start"):
            motor.startZero = True
            serialDevices[0].writeOut("start")
            stpCount = 0
            while (serialDevices[0].readIn() != "zero"):
                if (serialDevices[0].readIn() == "zero"):
                    break
            while not motor.zeroDone:
                # If "stp" command issued 50 times, read clearCore output for "done" msg
                if (stpCount > 50):
                    motor.zeroDone = True
                    serialDevices[0].writeOut("stpFinal")
                    break
                else:
                    # Call on readDial function passing micro.port initialized in class constructor
                    input = serialComm.readDial(serialDevices[1].port)
                    out = formatMsg(input)
                    serialDevices[0].writeOut(out)
                    if (out == "stp"):
                        stpCount += 1
                    else:
                        stpCount = 0
    serialDevices[0].writeOut("done")

# Handles running a set of moves w/ same amount of steps per move
# Issues clearCore steps to move after taking a reading 

# 128000, 31 almost full travel 4.8 meters | 819200, 4 3.84 meters
# 128000, 20 3 meters | 1280000, 1 1.5 meters

def runOneMove(motor, serialDevices, stepsAdjusted):
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

#def calcLaserOffset(laserReading, ):

def runMoves(steps, amountOfSteps, motor, serialDevices, straightHome = True):
    serialComm.initializeLaser(serialDevices[2].port)
    time.sleep(2)
    dial = serialComm.readDial(serialDevices[1].port)

    initialLaser = serialComm.readLaser(serialDevices[2].port)
    laserReadSt = initialLaser
    totalLaser = 0

    data = []

    # amountOfSteps+1 for returning back to zero in one move, 
    # amountOfSteps*2 for returning back to zero in same amount of moves & steps per move
    if straightHome:
        stepsRange = amountOfSteps+1
        stepMulti = amountOfSteps*-1
    else:
        stepsRange = amountOfSteps*2
        stepMulti = -1

    for i in range(stepsRange):
        print(f"Start laser = {laserReadSt}m")
        stepsAdjusted = steps
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*stepMulti)

        runOneMove(motor, serialDevices, stepsAdjusted)
        
        time.sleep(5)
        laserReadEnd = serialComm.readLaser(serialDevices[2].port)
        laserDist = float(laserReadEnd) - float(laserReadSt)
        mmDistance = mathFunc.calcDist(6400, stepsAdjusted)
        meterDistance = float(mmDistance / 1000)
        calcDiff = meterDistance - laserDist
        laserReadSt = serialComm.readLaser(serialDevices[2].port)

        print(f"\nEnd laser = {laserReadEnd}m\nLaser distance = {laserDist}m\n")
        #print(f"Steps distance = {meterDistance}m\nSteps distance - laser distance = {calcDiff*1000}mm\n")

        dataMove = {"steps": stepsAdjusted,
                    "dial": dial,
                    "laser": laserDist,
                    "calcMeters": meterDistance} 
        data.append(dataMove)

        time.sleep(0.5)
        # If the move isn't a returning to zero move, then count as cumulative measurement

        totalLaser = float(laserReadEnd) - float(initialLaser)
        totalStep = float(mathFunc.calcDist(6400, steps * (i + 1))/1000)
        print(f"\nTotal laser distance = {totalLaser}m")
        #print(f"Total calcualted step distance = {totalStep}m")
        #print(f"Total calculated steps - total laser distance = {(float(totalStep) - float(totalLaser))*1000}mm\n")
        input("Press Enter to continue...")
        time.sleep(5)
    return data