# This function test verifies zeroing, Pi-clearCore serial communication, serial devices,
# reading collection, and issuing of moves to clearCore

from piGantry.piSerial import serialInter as serialComm
from piGantry.piSerial import motorFunc

#python -m tests.serialInterTest.py

# Initialize new motor object for state management
motorX = motorFunc.motor()
motorY = motorFunc.motor()

motorGroup = (motorX, motorY)

# Initialize new serialObject instances for each device
microX = serialComm.serialObject(9600, "COM13")    
microY = serialComm.serialObject(9600, "COM14")  
clearCoreX = serialComm.serialObject(1000000, "COM18")
clearCoreY = serialComm.serialObject(1000000, "COM7")


# serialDevices should be tuple of 2 devices, (clearCoreX, clearCoreY, micro)
#serialDevices = (clearCoreX, clearCoreY, micro)

print("Zero X started!")
motorFunc.runZero(motorX, (clearCoreX, microX), 2)
print("Zero X finished!")
print("Zero Y started!")
motorFunc.runZero(motorY, (clearCoreY, microY), 4)
print("Zero Y finished!")

#motorFunc.runZero(motorY, clearCoreY, microZero=False)

# 819200, 6400 for 0.96 m | 1638400, 12800 for 0.96 m | 3276800, 25600 for 0.96 m
print(motorFunc.runMoves((409600, 4), motorGroup, (clearCoreY, clearCoreX, microY), steps2 = (163840, 3)))
#print(motorFunc.runMoves((819200, 4), motorY, clearCoreY, straightHome = False))
print("runMoves finished!")


