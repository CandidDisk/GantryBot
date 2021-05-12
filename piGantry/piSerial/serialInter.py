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
    #Laser rangefinder requires write "iACM" before it starts sending reading
    port.write("iACM".encode('utf-8'))

    #Flushing input buffer as laser rangefinder output buffer is quite large
    #Not flushing the input will result in delayed readings
    port.flushInput()
    port.flushOutput()

    #Giving time for laser rangefinder to fill buffer
    time.sleep(0.5)

    unformatLaser = port.read_until()
    sendLaser = unformatLaser.decode("ascii").strip()
