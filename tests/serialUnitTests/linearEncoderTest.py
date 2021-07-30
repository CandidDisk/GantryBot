# This function test verifies zeroing, Pi-clearCore serial communication, serial devices,
# reading collection, and issuing of moves to clearCore

from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc

import time
import threading
#python -m tests.serialInterTest.py

# Initialize new motor object for state management
motorX = motorFunc.motor(19.98145313)
motorY = motorFunc.motor(19.98626075)

motorGroup = (motorX, motorY)

#COM9 bluetooth arduino encoder Y Axis
#COM12 bluetooth arduino encoder X Axis

# Initialize new serialObject instances for each device
microX = serialComm.serialObject(9600, "COM13")    
#microY = serialComm.serialObject(9600, "COM14")  
clearCoreX = serialComm.serialObject(1000000, "COM18")
#clearCoreY = serialComm.serialObject(1000000, "COM7")
arduinoEncoder = serialComm.serialObject(9600, "COM12", timeout=0.3)



# serialDevices should be tuple of 2 devices, (clear
# CoreX, clearCoreY, micro)
#serialDevices = (clearCoreX, clearCoreY, micro)

print("Zero X started!")
motorFunc.runZero(motorX, (clearCoreX, microX), 2)
print("Zero X finished!")
#print("Zero Y started!")
#motorFunc.runZero(motorY, (clearCoreY, microY), 4)
#print("Zero Y finished!")

#motorFunc.runZero(motorY, clearCoreY, microZero=False)

# 819200, 6400 for 0.96 m | 1638400, 12800 for 0.96 m | 3276800, 25600 for 0.96 m
#print(motorFunc.runMoves((409600, 4), motorGroup, (clearCoreY, clearCoreX, microY), steps2 = (163840, 3)))

#arduinoEncoder.writeOut("zero")
serialComm.zeroArduinoEncoder(arduinoEncoder)
time.sleep(5)
print(serialComm.readArduinoEncoder(arduinoEncoder))


#while valEncoder != 0:
#    valEncoder = serialComm.readArduinoEncoder(arduinoEncoder)
#    if valEncoder:
#        print(valEncoder)

# 6547000, 1
# 395000, 20

print(motorFunc.runMoves((378000, 19), motorX, clearCoreX, straightHome = True, encoder=(False, arduinoEncoder), compensation=False))
#for i in range(2):
#    motorFunc.runOneMove(motorX, clearCoreX, 200)
#    motorFunc.runOneMove(motorX, clearCoreX, -200)
#print("Take reading!")
#print(serialComm.readArduinoEncoder(arduinoEncoder))
#print("runMoves finished!")

#while True:
#    valEncoder = serialComm.readArduinoEncoder(arduinoEncoder)
#    print(valEncoder)

