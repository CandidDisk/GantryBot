import serial
import time

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

#========================
#========================
    # the functions

def setupSerial(baudRate, serialPortName, name):
    
    if name==1:
        global serialPort
        serialPort = serial.Serial(port= serialPortName, baudrate = baudRate, timeout=0, rtscts=True)
        
    elif name==2:
        global micro
        micro = serial.Serial(port= serialPortName, baudrate = baudRate, timeout=0, rtscts=True)
    elif name==3:
        global laser
        laser = serial.Serial(port= serialPortName, baudrate = baudRate, timeout=0, rtscts=True)

    
    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))


setupSerial(9600, "/dev/ttyUSB1", 2)
setupSerial(38400, "/dev/ttyUSB0", 3)
laser.write("iACM".encode('utf-8'))

while True:
    
    bytesToRead1 = micro.inWaiting()
    bytesToRead2 = laser.inWaiting()
    #print(bytesToRead1)
    if bytesToRead1 > 0:
       x1 = micro.read(bytesToRead1).decode("utf-8")
       print(x1)
       print("\n")
    #x1 = laserRange.read().decode("utf-8")
    #print(x1)

            # check for a reply
    #if bytesToRead2 > 0:
    #    x2 = laser.read(bytesToRead2)
    #    sliced = x2[2:7]
    #    print(sliced)
    #    print("\n")

            
        
        
        # send a message at intervals

        

