import serial
import time


def __init__(self):
    self.newDataOut = False
    self.newDataIn = False

def setupSerialPort(baudRate, serialPortName):
    return serial.Serial(serialPortName, baudrate = baudRate, timeout= 10,  write_timeout=10, rtscts = False)

def writeOut(self, port, msg):
    msg = msg + '\n'
    out = msg.encode("ascii")
    port.write(out)
    self.newDataOut = True

def readIn(self, port):
    msgInString = "no new message"
    if (port.inWaiting() > 0):
        msg = port.read_until()
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

def readLaser(self, port):
    #Laser rangefinder requires write "iACM" before it starts sending reading
    port.write("iACM".encode('utf-8'))

    #Flushing input buffer as laser rangefinder output buffer is quite large
    #Not flushing the input will result in delayed readings
    port.flushInput()
    port.flushOutput()

    #Giving time for laser rangefinder to fill buffer
    time.sleep(0.5)

    unformatLaser = laserRange.read_until()
    sendLaser = unformatLaser.decode("ascii").strip()