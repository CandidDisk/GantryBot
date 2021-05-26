import serial
import time

class serialObject(object):
    def __init__(self, baudRate, serialPortName):
        self.newDataOut = False
        self.newDataIn = False
        self.confirmMessage = False
        self.port = serial.Serial(serialPortName, baudrate = baudRate, timeout= 10,  write_timeout=10, rtscts = False)

    def writeOut(self, msg):
        msg = msg + '\n'
        out = msg.encode("ascii")
        self.port.write(out)
        self.newDataOut = True

    def readIn(self):
        msgInString = "no new message"
        if (self.port.inWaiting() > 0):
            msg = self.port.read_until()
            msgInString = msg.decode("ascii").strip()
            self.newDataIn = True
            return msgInString
        else:
            self.newDataIn = False
        return msgInString
            
def readDial(port):
    bytesToReadDial = port.inWaiting()
    if (bytesToReadDial > 8):
        slicedDial = port.read(bytesToReadDial)[0:9]
        sendDial = str(slicedDial)
        return sendDial

def readLaser(port):
    # Needs to call on initializeLaser once prior to reading
    bytesToRead = port.inWaiting()
    if bytesToRead > 10:
        inputLaser = port.read(bytesToRead).decode("utf-8", "ignore")
        slicedLaser = inputLaser[1:8]
        return slicedLaser

def initializeLaser(port):
    # Laser rangefinder requires write hex start addr before it starts sending reading
    while port.inWaiting() == 0:
        packet = b'\x80\x06\x03\x77'
        port.write(packet)
        time.sleep(0.2)
        print("waiting..!")