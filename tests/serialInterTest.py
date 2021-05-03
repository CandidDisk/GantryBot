from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
from piGantry.piSerial import mathFunc
import serial
import time
import threading

#python -m tests.serialInterTest.py


micro = serialComm.serialObject(9600, "COM9")    
clearCore = serialComm.serialObject(1000000, "COM18")
motor = motorFunc.motor()

def runZero():
    while not motor.startZero:
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            while not motor.zeroDone:
                print(clearCore.readIn())
                if (clearCore.readIn() == "done"):
                    motor.zeroDone = True
                    clearCore.writeOut("done")
                    break
                else:
                    input = serialComm.readDial(micro.port)
                    out = motorFunc.formatMsg(input)
                    clearCore.writeOut(out)

def runMoves():
    steps = 0
    msg = "no msg"
    lastMsg = clearCore.readIn()
    if (lastMsg == "move"):
        motor.moveRead = True
    if (moveReady):
        temp = "not"

        while (temp != "q"):
            if (lastMsg == "move1"):
                steps = "+640000"
            if (lastMsg == "move1z"):
                steps = "-640000"
                distFromZero = 0
            if (lastMsg == "move2"):
                steps = "+2560000"
            if (lastMsg == "move2z"):
                steps = "-2560000"
                distFromZero = 0

            temp = input("\nPress q to send continue move | w to take read | r to skip: ")
            if (temp == "r"):
                break
            if (temp == "w"):
                dial = serialComm.readDial(micro.port)

                mmDistance = mathFunc.calcDist(6400, steps)
                meterDistance = float(mmDistance) / 1000


runZero():

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