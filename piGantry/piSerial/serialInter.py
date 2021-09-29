import serial
import time

class serialObject(object):
    def __init__(self, baudRate, serialPortName, timeout=1, writeTimeOut= 3):
        self.newDataOut = False
        self.newDataIn = False
        self.confirmMessage = False
        # Initialize serial object
        self.port = serial.Serial(serialPortName, baudrate = baudRate, timeout= timeout,  write_timeout=writeTimeOut, rtscts = False)

    # Writes message out to serial port
    def writeOut(self, msg):
        try:
            msg = msg + '\n'
            out = msg.encode("ascii")
            self.port.write(out)
            self.newDataOut = True
        except:
            print("Write failed, trying again")

    def readIn(self, sendMsg = False):
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
                if sendMsg:
                    print(f"No input, sending msg : {sendMsg}")
                    self.writeOut(sendMsg)
                    time.sleep(0.01)

# Sends command to cart onboard arduino to reset encoder counter
def zeroArduinoEncoder(encoder):
    zeroDone = False
    while not zeroDone:
        encoder.writeOut("zero")
        time.sleep(0.2)
        msg = encoder.readIn(sendMsg = "zero")
        if (msg == "zero"):
            zeroDone = True
            break

def readArduinoEncoder(encoder):
    encoder.writeOut("read")
    valEncoder = False
    encoder.port.flushInput()
    encoder.port.flushOutput()
    while not valEncoder:
        print(encoder.port.inWaiting())
        if encoder.port.inWaiting() > 0:
            valEncoder = encoder.port.readline().decode().strip()
            return (float(valEncoder)*5)*1e-6
        else:
            encoder.writeOut("read")
        time.sleep(0.5)


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
        
        