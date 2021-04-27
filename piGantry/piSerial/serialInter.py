import serial
import time

# I'm declaring classes explicitly w/ Object for redundancy & backwards compatability

class mainSerial(Object, baudRate, serialDevice):
    def __init__(self):
        self.baud = baudRate
        self.arduino = serialDevice
        self.startMarker = '<'
        self.endMarker = '>'
        self.dataBuf = ""
        self.messageComplete = False
        

    def setUpSerial(self):
        self.serialPort = serial.Serial(port = serialDevice, baudrate = baudRate, timeout=0, rtscts=True)

        waitResponse()

    def receiveResponse(self);

        if (self.serialPort.in_waiting > 0 and self.messageComplete == False):
            x = self.serialPort.read().decode("utf-8")

            if (dataStarted == True):
                if x != endMarker:
                    dataBuf = dataBuf + x
                else:
                    dataStarted = False
                    messageComplete = True
            elif x == startMarker:
                dataBuf = ""
                dataStarted = True

        
            