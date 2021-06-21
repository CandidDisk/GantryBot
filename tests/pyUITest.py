from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import pyGUI
from piGantry.piSerial import mathFunc
from piGantry.piSerial import motorFunc

pyUI = pyGUI.uiSTATE()

def main(uiClass, debugMode=True):
    motorX = motorFunc.motor()
    motorY = motorFunc.motor()

    motorGroup = (motorX, motorY)
    if (not debugMode):
        microX = serialComm.serialObject(9600, "COM13")    
        microY = serialComm.serialObject(9600, "COM14")  
        clearCoreX = serialComm.serialObject(1000000, "COM18")
        clearCoreY = serialComm.serialObject(1000000, "COM7")
    else:
        microX, microY, clearCoreX, clearCoreY = "fooo"
        uiClass.debugMode = True

    uiClass.mainPage(motorGroup, (microX, microY), (clearCoreX, clearCoreY))

main(pyUI)

print("hello")
