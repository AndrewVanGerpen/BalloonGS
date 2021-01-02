from ctypes import windll.shcore # Library that looks for device display scaling settings so the GUI is not blurry
from tkinter import * # Graphical Library
from tkinter import ttk
import datetime

windll.shcore.SetProcessDpiAwareness(1) #Line to find display scaling

import packagedGUI.fileIO
import packagedGUI.db
import packagedGUI.serialInterface

masterFile = packagedGUI.fileIO.initMasterOutputFile()

def choosePort():
    i=0
    while (i < len(ports)): # this is janky but I think it is the only real way to make buttons for each available COM port, add a way to refresh this list
        global k
        k = len(ports)
        if(i==0):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'), command = lambda: mySerial(0)).grid(row=0, column=0, padx=4, sticky="W")
        if(i==1):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda: mySerial(1)).grid(row=1, column=0, padx=4, sticky ="W")
        if(i==2):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda: mySerial(2)).grid(row=2, column=0, padx=4, sticky ="W")
        if(i==3):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda:mySerial(3)).grid(row=3, column=0, padx=4, sticky ="W")
        if(i==4):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda:mySerial(4)).grid(row=4, column=0, padx=4, sticky ="W")
        if(i==5):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda: mySerial(5)).grid(row=5, column=0, padx=4, sticky ="W")
        if(i==6):
            Button(frame_comports, text=ports[i], height = 1, width = 40, font=('Helvetica', '12'),command = lambda: mySerial(6)).grid(row=6, column=0, padx=4, sticky ="W")
        i=i+1

def retrieveData():
    global p
    global data
    global canvas
    global vsb
    global fileList
    global frame_currentData
    global portsLength
    global currentTimeLabel

    if(serialInterface.dataInBuffer()): # potentially create function to ouput serial status
        frame_data.update_idletasks() # what does this mean again

        # Writing to local file
        masterFile.write(fileString + '\n')

        uniquePayloadCheck = True

        # Check if most recent payload ID has been logged yet
        for y in range(len(uniquePayloads)):
            if uniquePayloads[y] == fileList[0]:
                uniquePayloadCheck = False
                payloadIndex = y

        if uniquePayloadCheck:
            try:
                uniquePayloads.append(fileList[0])
                fileTime = fileList[0] + "_Payload.csv" # create the file name in the "day folder" that is labeled with the exact time
                payloadFileName.append(os.path.join(fileDay, fileTime)) # merge folder and file
                payloadFile.append(open(payloadFileName[-1],'a+'))
                payloadIndex = length(uniquePayloads)-1

            except:
                pass #if this doesnt work, dont crash (not critical per say)

        payloadFile[payloadIndex].write(fileString + '\n')

        if(upload.get()==1 and len(fileList)<=15): # checks to see if data upload checkbox is selected and the length of the string is less than or equal to 12 variables
            packagedGUI.db.writedb()   # writes to server database if button is selected

        canvas.config(scrollregion=canvas.bbox("all"))
        if(scroll.get()==1):
            canvas.yview_moveto(1)

    guiTime = datetime.datetime.now()
    try:
        currentTimeLabel.destroy()
    except:
        pass
    currentTimeLabel = Label(frame_comports, text = "Current Time: " + str(guiTime.strftime('%H:%M:%S')), font= ('Helvetica', '16'), bg ="maroon", fg = "gold")
    currentTimeLabel.grid(row = len(header)+portsLength+2, column=0, sticky='sw')
    root.after(100,retrieveData) # rerun function after this many ms

frame_main = Frame(root,bg="maroon") # create a frame in root
frame_main.grid(sticky='news') # idk

Welcome = Label(frame_main, text = "MNSGC Ballooning", font=('Helvetica', '26'), bg="maroon", fg="white")
Welcome.grid(row=0, column=0, sticky = 'nw')

if internetConnection==True:
    connectionMessage = "Online"
else:
    connectionMessage = "Offline"

connectionLabel = Label(frame_internet, text = connectionMessage, font=('Helvetica', '16'), bg="maroon", fg="lightgray")
connectionLabel.grid(row=0, column=0, sticky = 'nw')

upload = IntVar() # variable that the checkbutton will control
if(internetConnection==True):
    upload.set(1)
dataUpload = Checkbutton(frame_internet, text="Upload to Server?", selectcolor = "black", bg="maroon", fg= "gold", font=('Helvetica', '12'), variable = upload)
dataUpload.grid(row=0,column=1, sticky = 'nw')

node = IntVar()
node.set(1)
Radiobutton(frame_internet, text="Node 1", font=('Helvetica', '14'), selectcolor = "black", bg="maroon", fg="lightgray", variable=node, value=1).grid(row=1,column=0, sticky = 'nw')
Radiobutton(frame_internet, text="Node 2", font=('Helvetica', '14'), selectcolor = "black", bg="maroon", fg="lightgray", variable=node, value=2).grid(row=2,column=0, sticky = 'nw')
Radiobutton(frame_internet, text="Node 3", font=('Helvetica', '14'), selectcolor = "black", bg="maroon", fg="lightgray", variable=node, value=3).grid(row=3,column=0, sticky = 'nw')

frame_comports = Frame(frame_main, bg = "maroon")
frame_comports.grid(row=2, column = 0, sticky = 'nw')

frame_canvas = Frame(frame_main) # create a new frame in the main frame
frame_canvas.grid(row=1, column=1, rowspan = 30, sticky='nw') # place the canvas rowspan = 10,
columns_width = 800
rows_height = 300

wazzup = ["2021", "iz", "great"]
header = ["Payload", "Date","Time", "Lat", "Long","Alt(ft)","Sensor1","Sensor2", "Sensor3","Sensor4","Sensor5","millis()","additional messages"]; # GUI header

# build out data table with scroll bar
tv = ttk.Treeview(frame_canvas, columns = (1,2,3,4,5,6,7,8,9,10,11,12,13), show = "headings", height = "5")

for x in header:
    tv.heading(header.index(x) , text = x)
    tv.column(header.index(x),minwidth=0,width=100) 

tv.grid(row=0, column=0, sticky="news")

vsb = Scrollbar(frame_canvas, orient="vertical", command = tv.yview) # create a scroll bar in the text canvas
vsb.grid(row=0,column=1,sticky='ns') # Place the verical scroll bar
tv.configure(yscrollcommand=vsb.set) # set the vertical scroll bar

frame_canvas.config(width=columns_width + vsb.winfo_width(), height= rows_height, bg="maroon")

scroll = IntVar() # variable that the checkbutton will control
scrollOrNot = Checkbutton(frame_canvas, text="Autoscroll", selectcolor = "black", bg="maroon", fg= "gold", font=('Helvetica', '14'), variable = scroll)
scrollOrNot.grid(row=1,column=0, sticky = 'ne')

frame_command = Frame(frame_canvas, bg = "maroon")
frame_command.grid(row = 2, column = 0, sticky = 'nw')

# build out data send box
payloadIDLabel = Label(frame_command, text = "Payload ID:" ,  bg="maroon", fg= "gold", font=('Helvetica', '18')).grid(row=0, column=0, sticky="sw")
payloadID = Entry(frame_command, font=('Helvetica', '18'), width = 10)
payloadID.grid(row=0, column=1, sticky="sw")
commandLabel = Label(frame_command, text = "Command:" ,  bg="maroon", fg= "gold", font=('Helvetica', '18')).grid(row=0, column=2, sticky="sw")
commandText = Entry(frame_command,font=('Helvetica', '18'), width = 16)
commandText.grid(row=0, column=3, sticky="sw")
sendCommand = Button(frame_command, text = "SEND", font=('Helvetica', '12'), width = 10, command = lambda: send()).grid(row=0,column=4, padx = 5, sticky="sw")

root.mainloop()
