# This function test verifies zeroing, Pi-clearCore serial communication, serial devices,
# reading collection, and issuing of moves to clearCore

from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc
import serial
import time

#python -m tests.serialInterTest.py

# Initialize new motor object for state management
motor = motorFunc.motor()

# Initialize new serialObject instances for each device
micro = serialComm.serialObject(9600, "COM21")    
clearCore = serialComm.serialObject(1000000, "COM18")
laser = serialComm.serialObject(9600, "COM16", timeout=10, writeTimeOut=10)

# serialDevices should be tuple of 3 devices, (clearCore, micro, laser)
serialDevices = (clearCore, micro, laser)

motorFunc.runZero(motor, serialDevices)

print(motorFunc.runMoves(819200, 4, motor, serialDevices))
print("finished!")


