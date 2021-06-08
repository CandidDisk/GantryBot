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
micro = serialComm.serialObject(9600, "COM13")    
clearCore = serialComm.serialObject(1000000, "COM18")
laser = serialComm.serialObject(9600, "COM16", timeout=10, writeTimeOut=10)

# serialDevices should be tuple of 3 devices, (clearCore, micro, laser)
serialDevices = (clearCore, micro, laser)

motorFunc.runZero(motor, serialDevices)

# 819200, 6400 for 0.96 m | 1638400, 12800 for 0.96 m | 3276800, 25600 for 0.96 m
print(motorFunc.runMoves(1638400, 4, motor, serialDevices, straightHome=True))
print("finished!")


