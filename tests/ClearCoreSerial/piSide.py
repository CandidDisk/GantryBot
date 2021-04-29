import serial

port = "/dev/ttyACM0"
baudrate = 115200

def setupSerial(baudRate, serialPortName, name):

    port = serial.Serial(serialPortName, baudrate = baudRate, timeout= 0, rtscts = True)

    if name == 1:
        global serialPort
        serialPort = port
        

    elif name == 2:
        global digDial
        digDial = port

    elif name == 3:
        global laserRange
        laserRange = port

def tell(msg):
    msg = msg + '\n'
    x = msg.encode('ascii') 
    serialPort.write(x)

def hear():
    msg = serialPort.read_until()
    mystring = msg.decode('ascii')
    return mystring

setupSerial(115200, "/dev/ttyACM0", 1)

while True:
    val = input()
    tell(val) 
    var = hear() 
    print(var) 