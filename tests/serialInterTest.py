# This function test verifies zeroing, Pi-clearCore serial communication, serial devices,
# reading collection, and issuing of moves to clearCore

from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc
import serial
import time

#python -m tests.serialInterTest.py

# Initialize new motor object for state management
motor = motorFunc.motor()

# Initialize new serialObject instances for each device
micro = serialComm.serialObject(9600, "COM8")    
clearCore = serialComm.serialObject(1000000, "COM18")

# This functional test is not using serialObject to declare the laser rangefinder,
# I haven't written proper lambda arguments for serialObject class to support new laser
laser = serial.Serial(port= "COM16", baudrate = 9600, bytesize=serial.EIGHTBITS, 
                      timeout=10, write_timeout=10, parity=serial.PARITY_NONE, 
                      stopbits=serial.STOPBITS_ONE, rtscts=False)



# Handles zeroing process by reading digital dial & issuing instructions to clearCore
def runZero():
    while not motor.startZero:
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            stpCount = 0
            while (clearCore.readIn() != "zero"):
                if (clearCore.readIn() == "zero"):
                    break
            while not motor.zeroDone:
                # If "stp" command issued 50 times, read clearCore output for "done" msg
                if (stpCount > 49 and clearCore.readIn() == "done"):
                    motor.zeroDone = True
                    clearCore.writeOut("done")
                    break
                else:
                    # Call on readDial function passing micro.port initialized in class constructor
                    input = serialComm.readDial(micro.port)
                    out = motorFunc.formatMsg(input)
                    clearCore.writeOut(out)
                    if (out == "stp"):
                        stpCount += 1


# Handles running a set of moves w/ same amount of steps per move
# Issues clearCore steps to move after taking a reading 
def runMoves(steps, amountOfSteps):
    
    serialComm.initializeLaser(laser)
    initialLaser = serialComm.readLaser(laser)
    totalLaser = 0

    # list of move data
    data = []

    # amountOfSteps+1 for returning back to zero in one move, 
    # amountOfSteps*2 for returning back to zero in same amount of moves & steps per move
    for i in range(amountOfSteps+1):
        stepsAdjusted = steps
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*amountOfSteps) * -1
        
        while (not motor.moveReady):
            if (clearCore.readIn() == "move"):
                motor.moveReady = True
                motor.moveDone = False
            

        if (motor.moveReady):
            dial = serialComm.readDial(micro.port)
            time.sleep(30)
            laserReadSt = serialComm.readLaser(laser)
            print(f"\nCurrent index {i}")
            clearCore.writeOut("move")
            print(f"Sent to clearCore move")
            clearCore.writeOut(f"{stepsAdjusted}")
            print(f"Sent to clearCore {stepsAdjusted} steps")
            motor.moveReady = False

        while (not motor.moveDone):
            if (clearCore.readIn() == "moveDone"):
                print("move done")
                motor.moveDone = True

        time.sleep(2)
        laserReadEnd = serialComm.readLaser(laser)
        laserDist = float(laserReadEnd) - float(laserReadSt)
        mmDistance = mathFunc.calcDist(6400, stepsAdjusted)
        meterDistance = float(mmDistance) / 1000
        calcDiff = meterDistance - laserDist

        print(f"Start laser = {laserReadSt}m\nEnd laser = {laserReadEnd}m\nLaser distance = {laserDist}m\n")
        print(f"Steps distance = {meterDistance}m\nSteps distance - laser distance = {calcDiff*1000}mm\n")

        dataMove = {"steps": stepsAdjusted,
                    "dial": dial,
                    "laser": laserDist,
                    "calcMeters": meterDistance} 
        data.append(dataMove)

        time.sleep(0.5)
        # If the move isn't a returning to zero move, then count as cumulative measurement
        if (stepsAdjusted > 0):
            totalLaser = float(laserReadEnd) - float(initialLaser)
            totalStep = float(mathFunc.calcDist(6400, steps * (i + 1)))/1000
            print(f"\nTotal laser distance = {totalLaser}m")
            print(f"Total calcualted step distance = {totalStep}m")
            print(f"Total calculated steps - total laser distance = {(float(totalStep) - float(totalLaser))*1000}mm\n")
        time.sleep(5)
    return data

runZero()

# 128000, 31 almost full travel 4.8 meters
# 128000, 20 3 meters

print(runMoves(1280000, 1))
print("finished!")


