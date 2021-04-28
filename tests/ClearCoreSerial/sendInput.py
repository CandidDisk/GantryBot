import serial
import time
import threading


zeroDone = True

runZeroStat = True

newData = False

msgInString = "no msg"

lastMsg = "nothing"

sendDial = "no dial"


def setupSerialPort(baudRate, serialPortName, name):

    port = serial.Serial(serialPortName, baudrate = baudRate, timeout= 10,  write_timeout=10, rtscts = False)

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
    print("output msg {0}".format(out))
    serialPort.write(out)

def readFromCC():
    global zeroDone
    global newData 
    global msgInString
    global lastMsg
    while True:
        #read_until() more convenient than waiting for bytes? Not sure how blocking
        if (serialPort.inWaiting() > 0):
            #this reads even when port is unavailable, hence blocking occurs w/o inWaiting conditional
            msg = serialPort.read_until()
            msgInString = msg.decode('ascii').strip()
            lastMsg = msgInString
            #msgInString
            print("received msg {0}\n".format(msgInString))
            if (msgInString == "start"):
                zeroDone = False
                print("zero start! {0}".format(zeroDone))
                sendToCC(msgInString)
            if (msgInString == "done"):
                sendToCC(msgInString)
            newData = True
        else:
            newData = False


def zeroFunc():
    global sendDial

    one = int(sendDial[6])
    tenth = int(sendDial[8])
    hundredth = int(sendDial[9])
    thousandth = int(sendDial[10])

    print("\n")
    print(one)
    print(".")
    print(tenth)
    print(hundredth)
    print(thousandth)
    print("\n")

    outMsg = "no"

    if (one == 2):
        if (tenth+hundredth+thousandth == 0):
            outMsg = "stp"
            #print(readFromCC())
            print("\n")
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
    return outMsg


def setupSerial():
    setupSerialPort(1000000, "/dev/ttyACM0", 1)
    setupSerialPort(9600, "/dev/ttyUSB1", 2)
    setupSerialPort(38400, '/dev/ttyUSB0', 3)

    laserRange.write("iACM".encode('utf-8'))

    readThread = threading.Thread(target=readFromCC)
    readThread.start()


def runZero():

    global zeroDone
    global newData 
    global msgInString
    global lastMsg
    global sendDial
    global runZeroStat

    setupSerial()

    while runZeroStat:
        
        if (lastMsg != "nothing"):
            print(lastMsg)

        #print(msgInString == "start")
        #readFromCC()

        while not zeroDone:
            #print("yesy")
            if (msgInString == "done"):
                zeroDone = True
                runZeroStat = False
                sendToCC(msgInString)
                print("break!!!")
                break
            else:
                

                #bytesToReadLaser = laserRange.inWaiting(``)

                #if bytesToReadLaser > 0:
                #    laser = laserRange.read(bytesToReadLaser)
                bytesToReadDial = digDial.inWaiting()
                #print(bytesToReadDial)

                if bytesToReadDial > 0:
                    slicedDial = digDial.read(bytesToReadDial)[0:9]
                    sendDial = str(slicedDial)
                    print(sendDial)
                    try:
                        print("zero done {0}".format(zeroDone))
                        sendToCC(zeroFunc())
                    except Exception as e:
                        print(e)

def main():
    runZero()
    
main()



    
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