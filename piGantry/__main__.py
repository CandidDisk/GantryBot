from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import pyGUI
from piGantry.piSerial import mathFunc
from piGantry.piSerial import motorFunc

ui = pyGUI.uiSTATE(debugMode=True)

def main():
    motorX = motorFunc.motor(19.98145313)
    motorY = motorFunc.motor(19.98626075)

    motorGroup = (motorX, motorY)

    #microX = serialComm.serialObject(9600, "COM13")    
    #microY = serialComm.serialObject(9600, "COM14")  
    #clearCoreX = serialComm.serialObject(1000000, "COM18")
    #clearCoreY = serialComm.serialObject(1000000, "COM7")

    microX = 1    
    microY = 1 
    clearCoreX = 1
    clearCoreY = 1

    ui.mainPage(motorGroup, (microX, microY), (clearCoreX, clearCoreY))

main()

print("hello")
