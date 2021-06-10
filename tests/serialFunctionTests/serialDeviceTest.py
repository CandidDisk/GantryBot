# This function test is only for verifying serial devices

from piGantry.piSerial import serialInter as serialComm
import time
import csv


micro = serialComm.serialObject(9600, "COM21")
while True:
    input = serialComm.readDial(micro.port)
    print(input)


