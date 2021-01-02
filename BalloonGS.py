from ctypes import windll # Library that looks for device display scaling settings so the GUI is not blurry
from tkinter import * # Graphical Library
from tkinter import ttk

windll.shcore.SetProcessDpiAwareness(1) #Line to find display scaling

import packagedGUI.fileIO as fileIO
import packagedGUI.db as db
import packagedGUI.serialInterface as serialInterface

masterFile = fileIO.initMasterOutputFile()
BAUD = 57600 # Baud rate for most MNSGC RFD900 Units (Default baud for new firmware)

root = Tk() # label tkinter as root
root.title("Test GUI") # Title on window
root.grid_rowconfigure(0, weight=1) # weight here causes the row to take up more space than necessary
root.columnconfigure(0, weight=1) # ""

mainFrame = Frame(root,bg="maroon") #create a frame within the tkinter root
mainFrame.grid(sticky='news') # center the frame in the window

mainFrameHead = Label(mainFrame, text = "MNSGC Ballooning", font=('Helvetica', '26'), bg="maroon", fg="white")
mainFrameHead.grid(row=0, column=0, sticky = 'nw')

connectionFrame = Frame(mainFrame, bg = "maroon")
connectionFrame.grid(row=1, column = 0, sticky = 'nw')

connectionFrameLabel = Label(connectionFrame, text = db.connectionMessage, font=('Helvetica', '16'), bg="maroon", fg="lightgray")
connectionFrameLabel.grid(row=0, column=0, sticky = 'nw')

comPortsFrame = Frame(mainFrame, bg = "maroon")
comPortsFrame.grid(row=2, column=0, sticky = 'nw')

for m in serialInterface.ports:
    Button(comPortsFrame, text=m, height = 1, width = 40, font=('Helvetica', '12'), command = lambda: serialInterface.initComPort(serialInterface.ports.index(m),BAUD)).grid(row=serialInterface.ports.index(m), column=0, padx=4, sticky="W")

uploadData = IntVar()
if(db.internetConnection):
    uploadData.set(1)
dataUpload = Checkbutton(connectionFrame, text="Upload to Server?", selectcolor = "black", bg="maroon", fg= "gold", font=('Helvetica', '12'), variable = uploadData)
dataUpload.grid(row=0,column=1, sticky = 'nw')

dataFrame = Frame(mainFrame,bg='maroon') # create a new frame in the main frame
dataFrame.grid(row=1, column=1, rowspan = 30, sticky='nw') # place the canvas rowspan = 10,
columns_width = 800
rows_height = 300

style = ttk.Style()
style.configure("Treeview", font=(None, 13))
style.configure("Treeview.Heading", font=(None, 13))

header = ["Payload", "Date","Time", "Lat", "Long","Alt(ft)","Sensor1","Sensor2", "Sensor3","Sensor4","Sensor5","millis()","additional messages"]; # GUI header
dataTable = ttk.Treeview(dataFrame, columns = (0,1,2,3,4,5,6,7,8,9,10,11,12), show = "headings", height = "30", style="Treeview")
dataTable.grid(row=0, column=0,sticky="news")

for x in header:
    dataTable.heading(header.index(x), text=x)
    dataTable.column(header.index(x),minwidth=0,width=100)

verticalScrollbar = Scrollbar(dataFrame, orient="vertical", command = dataTable.yview)
verticalScrollbar.grid(row=0,column=1,sticky='ns') # Place the verical scroll bar
dataTable.configure(yscrollcommand=verticalScrollbar.set) # set the vertical scroll bar

scrollGrab = IntVar()
scrollOrNot = Checkbutton(dataFrame, text="Autoscroll", selectcolor = "black", bg="maroon", fg= "gold", font=('Helvetica', '14'), variable = scrollGrab)
scrollOrNot.grid(row=1,column=0, sticky = 'ne')

commandFrame = Frame(dataFrame,bg="maroon")
commandFrame.grid(row = 2, column = 0, sticky = 'nw')

# build out data send box
payloadIDLabel = Label(commandFrame, text = "Payload ID:" ,  bg="maroon", fg= "gold", font=('Helvetica', '18')).grid(row=0, column=0, sticky="sw")
payloadID = Entry(commandFrame, font=('Helvetica', '18'), width = 10)
payloadID.grid(row=0, column=1, sticky="sw")
commandLabel = Label(commandFrame, text = "Command:" ,  bg="maroon", fg= "gold", font=('Helvetica', '18')).grid(row=0, column=2, sticky="sw")
commandText = Entry(commandFrame,font=('Helvetica', '18'), width = 16)
commandText.grid(row=0, column=3, sticky="sw")
sendCommand = Button(commandFrame, text = "SEND", font=('Helvetica', '12'), width = 10, command = lambda: serialInterface.sendCommand(payloadID.get(), commandText.get()))
sendCommand.grid(row=0,column=4, padx = 5, sticky="sw")

def appLoop():
    if(serialInterface.dataInBuffer()):
        dataList, dataString = serialInterface.readSerialData()
        masterFile.write(dataString + '\n')

        dataTable.insert('','end',values = dataList)

        fileIO.writeIndividualPayloadFile(dataList, dataString)
        
        if(uploadData.get() and len(dataList)<=15): # checks to see if data upload checkbox is selected and the length of the string is less than or equal to 12 variables
            db.writedb()   # writes to server database if button is selected

        if(scrollGrab.get()):
            dataTable.yview_moveto(1)
    
    root.after(100,appLoop)

root.after(100,appLoop)
root.mainloop()