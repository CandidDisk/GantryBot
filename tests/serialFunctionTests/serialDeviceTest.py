# This function test is only for verifying serial devices

from piGantry.piSerial import serialInter as serialComm
import time
import csv


#micro = serialComm.serialObject(9600, "COM8")
laser = serialComm.serialObject(9600, "COM16", timeout=10, writeTimeOut=10)

serialComm.initializeLaser(laser.port, continuous=False)

startTime = time.time()
csvArr = [["Laser reading1", "Laser reading2", "Laser reading3", "Timestamp (seconds)"]]
for i in range(20):
    time.sleep(20)
    read = serialComm.readLaser(laser.port, continuous=False)
    read2 = serialComm.readLaser(laser.port, continuous=False)
    read3 = serialComm.readLaser(laser.port, continuous=False)
    endTime = time.time()
    timeElapsed = endTime - startTime
    readingList = [read, read2, read3, timeElapsed]
    print(f"Laser = {read}, {read2}, {read3} | Time = {timeElapsed}")
    csvArr.append(readingList)
    #print(float(read) + 10)

with open("tests/serialFunctionTests/laserReading.csv", "w", newline='') as file:
    writeFile = csv.writer(file)
    writeFile.writerows(csvArr)
        

