from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc
import serial
import time

#python -m tests.serialInterTest.py

motor = motorFunc.motor()
micro = serialComm.serialObject(9600, "COM8")    
clearCore = serialComm.serialObject(1000000, "COM18")
laser = serial.Serial(port= "COM16", baudrate = 9600, bytesize=serial.EIGHTBITS, 
                      timeout=10, write_timeout=10, parity=serial.PARITY_NONE, 
                      stopbits=serial.STOPBITS_ONE, rtscts=False)

data = []


def runZero():
    while not motor.startZero:
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            #print("cool")
            stpCount = 0
            while (clearCore.readIn() != "zero"):
                if (clearCore.readIn() == "zero"):
                    break
            while not motor.zeroDone:
                #print(clearCore.readIn())
                if (stpCount > 1 and clearCore.readIn() == "done"):
                    motor.zeroDone = True
                    clearCore.writeOut("done")
                    break
                else:
                    input = serialComm.readDial(micro.port)
                    #print(input)
                    out = motorFunc.formatMsg(input)
                    #print(out)
                    clearCore.writeOut(out)
                    if (out == "stp"):
                        stpCount += 1

def runMoves(steps, amountOfSteps):
    serialComm.initializeLaser(laser)
    initialLaser = serialComm.readLaser(laser)
    totalLaser = 0

    for i in range(amountOfSteps+1):
        stepsAdjusted = steps
        if (i >= amountOfSteps):
            stepsAdjusted = (steps*amountOfSteps) * -1
        msg = "no msg"
        
        while (not motor.moveReady):
            if (clearCore.readIn() == "move"):
                motor.moveReady = True
                motor.moveDone = False
            

        if (motor.moveReady):
            dial = serialComm.readDial(micro.port)
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
        print(f"Start laser = {laserReadSt}m")
        print(f"End laser = {laserReadEnd}m")
        laserDist = float(laserReadEnd) - float(laserReadSt)
        print(f"Laser distance = {laserDist}m\n")
        mmDistance = mathFunc.calcDist(6400, stepsAdjusted)
        meterDistance = float(mmDistance) / 1000
        calcDiff = meterDistance - laserDist
        print(f"Steps distance = {meterDistance}m\n")
        print(f"Steps distance - laser distance = {calcDiff*1000}mm\n")
        dataMove = {"steps": stepsAdjusted,
                    "dial": dial,
                    "laser": laserDist,
                    "calcMeters": meterDistance}
        data.append(dataMove)
        time.sleep(0.5)
        if (stepsAdjusted > 0):
            totalLaser = float(laserReadEnd) - float(initialLaser)
    
            totalStep = float(mathFunc.calcDist(6400, steps * (i + 1)))/1000
            print(f"\nTotal laser distance = {totalLaser}m")
            print(f"Total calcualted step distance = {totalStep}m")
            print(f"Total calculated steps - total laser distance = {(float(totalStep) - float(totalLaser))*1000}mm\n")


runZero()
runMoves(128000, 20)
print(data)
print("finished!")


