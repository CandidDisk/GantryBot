# This function test is only for verifying serial devices

from piGantry.piSerial import serialInter as serialComm
import serial
import time


micro = serialComm.serialObject(9600, "COM8")
laser = serial.Serial(port= "COM16", baudrate = 9600, bytesize=serial.EIGHTBITS, timeout=10, write_timeout=10, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=False)


serialComm.initializeLaser(laser)

while True:
    laserRead = serialComm.readLaser(laser)        
    print(laserRead)
    print(serialComm.readDial(micro.port))
    time.sleep(0.1)

        

