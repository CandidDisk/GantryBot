import serial
import time

class serialObject(object):
    def __init__(self, baudRate, serialPortName, timeout=1, writeTimeOut= 10):
        self.newDataOut = False
        self.newDataIn = False
        self.confirmMessage = False
        # Initialize serial object
        self.port = serial.Serial(serialPortName, baudrate = baudRate, timeout= 1,  write_timeout=10, rtscts = False)

    def writeOut(self, msg):
        try:
            msg = msg + '\n'
            out = msg.encode("ascii")
            self.port.write(out)
            self.newDataOut = True
        except:
            print("Write failed, trying again")

    def readIn(self):
        msgInString = False
        while not msgInString:
            if (self.port.inWaiting() > 0):
                msg = self.port.read_until()
                # Strip special & escape characters from incoming message
                msgInString = msg.decode("ascii").strip()
                self.newDataIn = True
                return msgInString
            else:
                self.newDataIn = False

# Will collapse readDial & readLaser w/ DRY in mind   
def readDial(port):
    sendDial = False
    # Flush i/o to get updated readings
    port.flushInput()
    port.flushOutput()
    # Only return sendDial if reading is valid
    while not sendDial:
        bytesToReadDial = port.inWaiting()
        if (bytesToReadDial > 8):
            slicedDial = port.read(bytesToReadDial)[0:9]
            sendDial = str(slicedDial)
            return float(sendDial[2:11])

def readLaser(port, continuous=True):
    # Needs to call on initializeLaser once prior to reading
    slicedLaser = False
    # Flush i/o to get updated readings
    port.flushInput()
    port.flushOutput()
    time.sleep(0.1)
    if not continuous:
        port.write(b'\x80\x06\x02\x78')
    # Only return slicedLaser if reading is valid
    while not slicedLaser:
        bytesToRead = port.inWaiting()
        if bytesToRead > 10:
            inputLaser = port.read(bytesToRead).decode("utf-8", "ignore")
            slicedLaser = inputLaser[1:8]
            return slicedLaser
    if not continuous:
        port.write(b'\x80\x04\x02\x7A')


def initializeLaser(port, continuous=True):
    # Laser rangefinder requires write hex start addr before it starts sending reading
    while port.inWaiting() == 0:
        # Sets resolution to 0.1 mm 
        packetInit = b'\xFA\x04\x0C\x02\xF4'
        # Start continuous reading
        port.write(packetInit)
        time.sleep(0.2)
        if continuous:
            packetStart = b'\x80\x06\x03\x77'
            port.write(packetStart)
            print("waiting..!")
        
        