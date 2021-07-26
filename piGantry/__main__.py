from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import pyGUI
from piGantry.piSerial import mathFunc
from piGantry.piSerial import motorFunc

def main():
    motorX = motorFunc.motor()
    motorY = motorFunc.motor()

    motorGroup = (motorX, motorY)

    microX = serialComm.serialObject(9600, "COM13")    
    microY = serialComm.serialObject(9600, "COM14")  
    clearCoreX = serialComm.serialObject(1000000, "COM18")
    clearCoreY = serialComm.serialObject(1000000, "COM7")

    pyGUI.mainPage(motorGroup, (microX, microY), (clearCoreX, clearCoreY))

main()

print("hello")
