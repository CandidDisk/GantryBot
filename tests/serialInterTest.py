from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
import serial
import time
import threading

#python -m tests.serialInterTest.py


micro = serialComm.serialObject(9600, "COM9")    
clearCore = serialComm.serialObject(1000000, "COM18")
motor = motorFunc.zeroFunc()

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

runZero()

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