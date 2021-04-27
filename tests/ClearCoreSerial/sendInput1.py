import serial
import time
newData = False
zeroDone = False


def setupSerial(baudRate, serialPortName, name):

    port = serial.Serial(serialPortName, baudrate = baudRate, timeout= 10, rtscts = False)

    if name == 1:
        global serialPort
        serialPort = port
        

    elif name == 2:
        global digDial
        digDial = port

    elif name == 3:
        global laserRange
        laserRange = port

def sendToCC(msg):
    msg = msg + '\n'
    out = msg.encode('ascii')
    serialPort.write(out)

def readFromCC():
    #read_until() more convenient than waiting for bytes? Not sure how blocking
    msg = serialPort.read_until()
    inString = msg.decode('ascii')
    return inString


setupSerial(1000000, "/dev/ttyACM0", 1)
setupSerial(9600, "/dev/ttyUSB0", 2)
setupSerial(38400, '/dev/ttyUSB1', 3)

laserRange.write("iACM".encode('utf-8'))

while True:

    sendDial = "no dial"

    bytesToReadDial = digDial.inWaiting()
    bytesToReadLaser = laserRange.inWaiting()

    if bytesToReadLaser > 0:
        laser = laserRange.read(bytesToReadLaser)

    if bytesToReadDial > 0:
        
        slicedDial = digDial.read(bytesToReadDial)[0:9]
        sendDial = str(slicedDial)

        one = int(sendDial[6])
        tenth = int(sendDial[8])
        hundredth = int(sendDial[9])
        thousandth = int(sendDial[10])

        #print(one+tenth+hundredth+thousandth)
        #print(one)
        #print(".")
        #print(tenth)
        #print(hundredth)
        #print(thousandth)

        outMsg = "none"

        #if (one > 2):
        #    outMsg = "s0+"
        #else:
        if (zeroDone == False):
            if (one == 2):
                if (tenth+hundredth+thousandth == 0):
                    outMsg = "stp"
                    zeroDone = True
                else:
                    outMsg = "s0+"
            else:
                if (one == 1):
                    if (tenth > 7):

                        outMsg="s2-"
                    else:

                        outMsg = "s1-"

                else:
                    outMsg = "m0-"
            sendToCC(outMsg)

    if (zeroDone == True):
        received = readFromCC()
        print(received)
        print(laser)
        print("/n")
        print(sendDial)
        print("/n")
            


        #if (newData == False):
        
        #newData = True

        #if (newData == True):
        #received = readFromCC()
        #newData = False

        #print('\n')
        #print(received)
        #print('\n')
        
    
    
    



    
#    if bytesToReadSer > 0:
#        arduinoReply = serialPort.read()
#        print(arduinoReply)
#    else:
#        serialPort.write("hello".encode('utf-8'))

    #print("writing manual")

    #serialPort.write("hello".encode('utf-8'))

    #print("writing manual end")
        
        # send a message at intervals
    #if time.time() - prevTime > 1.0:
    #sendToArduino("this is a test ")
    #prevTime = time.time()
    #count += 1