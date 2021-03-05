import serial

#I'm declaring classes explicitly w/ Object for redundancy & backwards compatability

class mainSerial(Object, baudRate, serialDevice):
    def __init__(self):
        self.baud = baudRate
        self.arduino = serialDevice
        

    def setUpSerial(self):
        self.serialPort = serial.Serial(port = serialDevice, baudrate = baudRate, timeout=0)
    
    def waitResponse();