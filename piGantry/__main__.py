from piSerial import serialInter as serialComm

micro = serialComm.setupSerialPort(9600, "COM8")
while True:
    input = serialComm.readDial(micro)

    if (input != None):
        print(input)