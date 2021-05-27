from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc
import serial
import time
import threading

#python -m tests.serialInterTest.py

motor = motorFunc.motor()
micro = serialComm.serialObject(9600, "COM8")    
clearCore = serialComm.serialObject(1000000, "COM18")
laser = serial.Serial(port= "COM16", baudrate = 9600, bytesize=serial.EIGHTBITS, 
                      timeout=10, write_timeout=10, parity=serial.PARITY_NONE, 
                      stopbits=serial.STOPBITS_ONE, rtscts=False)

data = []

currentMsg = None

def readCC():
    global currentMsg
    currentMsg = clearCore.readIn()
    print(f"received msg = {currentMsg}")

def runZero():
    global currentMsg
    while not motor.startZero:
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            #print("cool")
            stpCount = 0
            while not motor.zeroDone:
                #print(clearCore.readIn())
                if (stpCount == 50 or currentMsg == "done"):
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
    global currentMsg
    serialComm.initializeLaser(laser)
    motor.moveReady = True

    for i in range(amountOfSteps*2):
        print(i)
        if i > amountOfSteps:
            steps = steps * -1
        msg = "no msg"
                
        if (motor.moveReady):
            inputUser = "not"

            while (input != "q"):
                inputUser = input("\nPress q to send continue move | w to take read | r to skip: ")
                if (inputUser == "r"):
                    break
                if (inputUser == "w"):
                    dial = serialComm.readDial(micro.port)
                    laserRead = serialComm.readLaser(laser)
                    while not laserRead:
                        laserRead = serialComm.readLaser(laser)
                        continue
                    mmDistance = mathFunc.calcDist(6400, steps)
                    meterDistance = float(mmDistance) / 1000
                    dataMove = {
                        "steps": steps,
                        "dial": dial,
                        "laser": laserRead,
                        "calcMeters": meterDistance
                    }
                    print(dataMove)
                    data.append(dataMove)
                if (inputUser == "q"):
                    clearCore.writeOut("move")
                    clearCore.writeOut(f"{steps}")

readThread = threading.Thread(target=readCC())
readThread.start()
runZero()
runMoves(128000, 5)
print(data)
print("finished!")

#while True:
#    input = serialComm.readDial(micro.port)
#    if (input != None):
#        print(motor.zeroDone)
#        print(input)
#        out = motorFunc.formatMsg(input)
#        print(out)
#        if (out == "stp"):
#            motor.zeroDone = True