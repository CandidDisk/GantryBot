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

# serialDevices should be tuple of 3 devices, (clearCore, micro, laser)
serialDevices = (clearCore, micro, laser)

motorFunc.runZero(motor, serialDevices)

print(motorFunc.runMoves(819200, 4, motor, serialDevices))
print("finished!")


