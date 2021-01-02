import mysql.connector
from mysql.connector import errorcode
try:
    import httplib
except:
    import http.client as httplib

internetConnection = False
connectionMessage = "Offline"

def checkInternet(): # check for internet connection
    global internetConnection
    global connectionMessage
    internetConn = httplib.HTTPConnection("www.google.com", timeout=3)
    try:
        internetConn.request("HEAD", "/")
        internetConn.close()
        internetConnection = True
        connectionMessage = "Online"
    except Exception as e:
        internetConnection = False
        connectionMessage = "Offline"

def connectdb():
    global cnx
    global cursor

    try:
        fileName = "loginInfo.txt"
        file = open(fileName,'r')
        lines = file.readlines()

        for x in lines:
            if x.startswith('user='):
                myUser = x[x.find('= ')+2:-1]
            if x.startswith('password='):
                myPassword = x[x.find('= ')+2:-1]
            if x.startswith('host='):
                myHost = x[x.find('= ')+2:-1]
            if x.startswith('database='):
                myDatabase = x[x.find('= ')+2:-1]

        cnx = mysql.connector.connect(user=myUser, password=myPassword, host=myHost,
                                    database=myDatabase)
        cursor = cnx.cursor()
    except:
        print("failed to connect to database")

def clearTable():
    try:
        sql = "DROP TABLE sensorDataOne"
        cursor.execute(sql)   
        createString = """CREATE TABLE sensorDataOne (
        id int NOT NULL AUTO_INCREMENT,
        payload text,
        gpsHour text,
        gpsMin text,
        gpsSecond text,
        latitude text,
        longitude text,
        altitude text,
        altGuess text,
        intTemp text,
        extTemp text,
        PRIMARY KEY(id))"""
        print(createString)
    
        cursor.execute(createString)
        cnx.commit()

    except:
        print("failed to connect to database")

def writedb(sensData, currentNodeVal):
    global cnx
    global cursor
    try:
        nodeLabels = ["One", "Two", "Three"] # node label list
        # SQL syntax to append data to current node
        add_sensorData = ("INSERT INTO sensorData" + nodeLabels[currentNodeVal-1] +
               "(payload, gpsDate, gpsTime, latitude, longitude, altitude, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        cursor.execute(add_sensorData, sensData)
        cnx.commit()
    except:
        print("failed to post data")

