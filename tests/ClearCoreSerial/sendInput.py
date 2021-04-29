import serial
import time
import threading
import json
import sys
from pathlib import Path

# There are a couple excess variables I forgot to take out during debugging

zeroDone = True

runZeroStat = True

newData = False

msgInString = "no msg"

lastMsg = "nothing"

sendDial = "no dial"

moveReady = False

moveMsg = "no msg"

mvtCount = 0

data = {}

# I didn't use proper constructors to handle scope since I wrote this 
# w/ the expectation of it being < 50 lines
# As I'm going to be cannibalizing this for proper "production" use, I'll update
# this once I finish serial & zeroing modules.
# Am using globals as temporary quick solution

# For all intents & purposes, current state of this test is fine. However, I need to revisit this
# post completion of outstanding modules before this can serve as a proper test case 

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
    global moveReady
    while True:
        #read_until() more convenient than waiting for bytes? Not sure how blocking
        if (serialPort.inWaiting() > 0):
            #this reads even when port is unavailable, hence blocking occurs w/o inWaiting conditional
            msg = serialPort.read_until()
            msgInString = msg.decode('ascii').strip()
            lastMsg = msgInString

            print("received msg {0}\n".format(msgInString))
            if (msgInString == "start"):
                zeroDone = False
                print("zero start! {0}".format(zeroDone))
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


def calcDist(stpPerTurn, steps):
    stepPerGBTurn = float(stpPerTurn) * 20 #20 = gear ratio
    stepPerMM = float(stepPerGBTurn) / 150 #150 = mm/turn
    traveledDistMM = float(steps) / float(stepPerMM)
    return traveledDistMM


def setupSerial():
    setupSerialPort(1000000, "/dev/ttyACM0", 1)
    setupSerialPort(9600, "/dev/ttyUSB0", 2)
    setupSerialPort(38400, '/dev/ttyUSB1', 3)

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

        while not zeroDone:
            if (msgInString == "done"):
                zeroDone = True
                runZeroStat = False
                sendToCC("done")
                break
            else:
                bytesToReadDial = digDial.inWaiting()
                if bytesToReadDial > 0:
                    slicedDial = digDial.read(bytesToReadDial)[0:9]
                    sendDial = str(slicedDial)
                    print(sendDial)
                    try:
                        print("zero done {0}".format(zeroDone))
                        sendToCC(zeroFunc())
                    except Exception as e:
                        print(e)

def runMoves():
    global moveReady
    global lastMsg
    global mvtCount
    steps = 0
    msg = "no msg"

    if ("move" in lastMsg):
        moveReady = True

    if (moveReady):
        temp = "not"

        if (lastMsg == "move1"):
            steps = "+640000"
        if (lastMsg == "move1z"):
            steps = "-640000"
        if (lastMsg == "move2"):
            steps = "+2560000"
        if (lastMsg == "move2z"):
            steps = "-2560000"

        while (temp != "q"):
            temp = input("\nPress q to send continue move | w to take read | r to skip: ")
            if (temp == "r"):
                break
            if (temp == "w"):

                digDial.flushInput()
                digDial.flushOutput()
                time.sleep(1)

                bytesToReadDial = digDial.inWaiting()

                if bytesToReadDial > 0:
                    slicedDial = digDial.read(bytesToReadDial)[0:9]
                    sendDial = str(slicedDial)
                    print("dial {0}".format(sendDial))

                laserRange.flushInput()
                laserRange.flushOutput()
                time.sleep(1)

                tempLaser = laserRange.read_until()
                laser = tempLaser.decode('ascii').strip()
                print("laser {0}".format(laser))

                print("steps {0}".format(steps))
                temp == "q"

                mmDistance = calcDist(6400, steps)
                print("calculated distance {0}".format(mmDistance))

                dataMove = {
                    int(mvtCount): {
                        "steps": steps,
                        "dial": sendDial,
                        "laser": laser,
                        "stepsToMM": mmDistance
                    }
                }
                data.update(dataMove)

                mvtCount += 1

            if (temp == "q"):
                print("sending {0}".format(lastMsg))
                sendToCC(lastMsg)
                moveReady = False

        temp = "not"
        
        while (temp != "e"):
            temp = input("\nPress e to save & exit | r to skip: ")
            if (temp == "r"):
                break
            if (temp == "e"):
                with open("data_file.json", "w") as write_file:
                    json.dump(data, write_file, indent=4) 
                sys.exit()

        sendToCC("not")
        

def main():
    runZero()
    print("zero done")
    while True:
        runMoves()
    
main()

