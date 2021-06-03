from piGantry.piSerial import serialInter as serialComm

laser = serialComm.serialObject(9600, "COM16", timeout=10, writeTimeOut=10)

serialComm.initializeLaser(laser.port)
print(serialComm.readLaser(laser.port))