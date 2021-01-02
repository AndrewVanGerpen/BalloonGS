import datetime # Library pulls the time from your device
import os
import csv # Library to read/write CSV files

uniquePayloads = []
uniquePayloadFileNames = []
uniquePayloadFiles = []
payloadIndex=0

def initMasterOutputFile():
    global fileDay

    today = datetime.datetime.now() # retrieve the current date and time from the local machine
    fileDay = "Data_" + today.strftime("%m-%d-%y") # create a file folder labeled with the date
    if os.path.exists(fileDay) == False: # if the folder does not exist with this name, make directory
        os.makedirs(fileDay)
    fileTime = "AllPayloads.csv"
    fileName =  os.path.join(fileDay, fileTime) # merge folder and file
    file = open(fileName,'a+') # Open CSV file to APPEND to
    return file

def writeIndividualPayloadFile(dataList, dataString):
    global uniquePayloads
    global payloadIndex

    uniquePayloadCheck = True

    for y in range(len(uniquePayloads)):
        if uniquePayloads[y] == fileList[0]:
            uniquePayloadCheck = False
            payloadIndex = y
    if uniquePayloadCheck:
        try:
            uniquePayloads.append(dataList[0])
            fileTime = dataList[0] + "_Payload.csv" # create the file name in the "day folder" that is labeled with the exact time
            uniquePayloadFileNames.append(os.path.join(fileDay, fileTime)) # merge folder and file
            uniquePayloadFiles.append(open(uniquePayloadFileNames[-1],'a+'))
            payloadIndex = len(uniquePayloads)-1
        except:
            pass # can have issues, but non-flight critical

    uniquePayloadFiles[payloadIndex].write(dataString + '\n')





    