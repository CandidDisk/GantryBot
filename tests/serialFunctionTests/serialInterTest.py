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


# Handles zeroing process by reading digital dial & issuing instructions to clearCore
def runZero():
    while not motor.startZero:
        if (clearCore.readIn() == "start"):
            motor.startZero = True
            clearCore.writeOut("start")
            stpCount = 0
            while (clearCore.readIn() != "zero"):
                if (clearCore.readIn() == "zero"):
                    break
            while not motor.zeroDone:
                # If "stp" command issued 50 times, read clearCore output for "done" msg
                if (stpCount > 49 and clearCore.readIn() == "done"):
                    motor.zeroDone = True
                    clearCore.writeOut("done")
                    break
                else:
                    # Call on readDial function passing micro.port initialized in class constructor
                    input = serialComm.readDial(micro.port)
                    out = motorFunc.formatMsg(input)
                    print(out)
                    clearCore.writeOut(out)
                    if (out == "stp"):
                        stpCount += 1
                    else:
                        stpCount = 0

motorFunc.runZero(motor, serialDevices)

print(motorFunc.runMoves(819200, 4, motor, serialDevices))
print("finished!")


