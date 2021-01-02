import serial.tools.list_ports # Accesses devices COM ports - install pyserial
import time # Library that allows time delays within the code

ports = serial.tools.list_ports.comports() # gather all serial ports
serialObj = serial.Serial()  # Global serial port. Declared later on after port is selected

def initComPort(number, BAUD_RATE): # number is the value from the button

    currentPort = str(ports[number])

    comPort = str(currentPort.split(' ')[0]) # Shortens the COM port + description (bluetooth, UART, etc.) to just the COM port

    serialObj.baudrate = BAUD_RATE # RFD900 radios
    serialObj.port = comPort # Declare the serial we are using with the correct COM port
    serialObj.open() # open the serial port to receive data

    time.sleep(1) # delay for a second so we can clear the port??

def sendCommand(payloadID, commandText):
    try:
        toSend = str(payloadID) + "?" + str(commandText) + "!"
        toSendBytes = bytes(toSend, 'utf-8')
        serialObj.write(toSendBytes)
        print("sent: " + toSend)
    except:
        print("command send failed")
        
def dataInBuffer():
    if serialObj.in_waiting > 2:
        return True
    else:
        return False

def readSerialData():
    recentData = serialObj.readline() # read last data line from the
    fileString = str(recentData).partition("!")[0] # eliminate exclamation mark and other characters associated with bowers xbee protocol
    fileString = fileString[fileString.find('b')+2:]
    fileString = fileString.replace(';',',')
    fileList = fileString.split(',') # split up the data string into a string list

    return fileList, fileString