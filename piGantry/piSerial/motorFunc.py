from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import mathFunc
import time

class motor():
    def __init__(self, gearRatio):
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
        self.gearRatio = float(gearRatio)

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
    startZero = False
    while not startZero:
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
        print("Waiting for move")
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
            print("Move done")
            motor.moveDone = True

# Runs one move to adjust to encoder reading

def adjustToEncoder(clearCore, motor, encoder, meterDistance):
    encoderReading = serialComm.readArduinoEncoder(encoder)
    print(f"encoder reading {encoderReading}")
    print(f"meter dist 1 {meterDistance - 0.0001}")
    print(f"meter dist 2 {meterDistance + 0.0001}")
    # While within threshold of resolution
    while ((meterDistance - encoderReading) > 0.1 or (meterDistance - encoderReading) > -0.1):
        # Finding difference between meter distance & encoder reading
        # & convert to steps
        encoderReading = serialComm.readArduinoEncoder(encoder)
        diff = (meterDistance - encoderReading) 
        stepsToTravel = mathFunc.calcDist(19200, diff, convertMMToSteps=True)
        # ClearCore doesn't execute fractional steps, must be greater than 1
        if stepsToTravel < 1: 
            break
        stepsToTravel = round(stepsToTravel)
        print(f"steps to travel {stepsToTravel} | diff {diff} | encoder reading {encoderReading}")
        runOneMove(motor, clearCore, stepsToTravel)
        time.sleep(0.3)

def runMoves(steps1, motorObj, serialDevices, steps2 = False, straightHome = True, encoder = False, jiggle = False, compensation = True):
    # amountOfSteps+1 for returning back to zero in one move, 
    # amountOfSteps*2 for returning back to zero in same amount of moves & steps per move

    wiggleHome = False
    if (type(serialDevices) is tuple):
        clearCore = serialDevices[0]
        clearCore2 = serialDevices[1]
    else:
        clearCore = serialDevices
    if (type(motorObj) is tuple):
        motor = motorObj[0]
        motor2 = motorObj[1]
    else:
        motor = motorObj
        
    # Amount of steps is steps to execute per move
    amountOfSteps = steps1[1]
    steps = steps1[0]
    # stepMulti is factor to multiply return to move steps by
    if straightHome:
        stepsRange = amountOfSteps+1
        # 
        stepMulti = amountOfSteps*-1
    else:
        stepsRange = amountOfSteps*2
        # Just convert steps to negative
        stepMulti = -1

    if (type(encoder) is tuple):
        encoderReader = encoder[1]

    correctionVal = 0
    totalCorrectionVal = 0
    for i in range(stepsRange):
        print(f"\n\nMove number: {i}\n")
        print("Move start")
        stepsAdjusted = steps
        print(f"Correction value: {correctionVal}")
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*stepMulti)-totalCorrectionVal
            #if not wiggleHome:
            #    for i in range(2):
            #        runOneMove(motor, clearCore, 200)
            #        runOneMove(motor, clearCore, -200)
            #wiggleHome = True
            print("Going home")
            print(serialComm.readArduinoEncoder(encoderReader))
            foo = input("Press Enter to continue...")
            #time.sleep(15)
        elif compensation:
            stepsAdjusted = stepsAdjusted + correctionVal
        correctionVal = 0

        mmDistance = mathFunc.calcDist(12800, stepsAdjusted, motor.gearRatio)
        meterDistance = float(mmDistance / 1000)
        totalStep = float(mathFunc.calcDist(12800, steps * (i + 1), motor.gearRatio)/1000)

        print(f"Total calcualted step distance 1 = {totalStep}m")
        if steps2:
            runMoves(steps2, motor2, clearCore2)
        runOneMove(motor, clearCore, (stepsAdjusted))
        if (not i >= amountOfSteps):
            if encoder:
                reading = serialComm.readArduinoEncoder(encoder[1])
                if encoder[0]:
                    time.sleep(5)
                    print(f"Encoder read 1: {reading}")
                    adjustToEncoder(clearCore, motor, encoder[1], meterDistance)
                    print("Adjust finished!")
                diff = (totalStep - reading)*1000
                print(f"Diff value: {diff}")
                print(f"Calculated dist: {totalStep} | Encoder read: {reading}")
                stepsToTravel = mathFunc.calcDist(19200, diff, motor.gearRatio, convertMMToSteps=True)
                stepsToTravel = round(stepsToTravel)
                if compensation:
                    if stepsToTravel > 1 or stepsToTravel < -1:
                        correctionVal = stepsToTravel
                    else:
                        correctionVal = 0
                    totalCorrectionVal += correctionVal
                print(f"Steps value: {stepsToTravel} | Correction Value: {correctionVal} | Total correction value: {totalCorrectionVal}")
                
        if jiggle:
            for i in range(2):
                runOneMove(motor, clearCore, 200)
                runOneMove(motor, clearCore, -200)
        if encoder[0]:
            print(f"Encoder read 2: {serialComm.readArduinoEncoder(encoder[1])}")
        #print("Take reading!")
        #time.sleep(15)
        print("Move end")
    return True