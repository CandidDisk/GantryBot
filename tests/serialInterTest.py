from piGantry.piSerial import serialInter as serialComm

def setupSerial():
    micro = serialComm.setupSerialPort(9600, "COM8")
    laser = serialComm.setupSerialPort(36000, "COM8")

while True:
    input = serialComm.readDial(micro)

    if (input != None):
        print(input)