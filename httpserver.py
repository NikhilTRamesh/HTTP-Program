#Nikhil Ramesh
#31499350
#Section 02
#! /usr/bin/env python3
# HTTP Server
import sys
import socket
import time
import struct
import os, os.path
import datetime, time
import codecs

#read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
cache = 'cache.txt' #cache file so that last-modified persists between client instants

def returnContent(fileName):
    formatString=''
    f=codecs.open(fileName, 'r', encoding='utf-8')
    data = f.read()
    for Line in data.split("\n"):
        if '<p class="p1">' in Line:
            formatString+= Line
    formatString=formatString.replace('<p class="p1">', '')
    formatString=formatString.replace('</p>','')
    formatString=formatString.replace('&lt;','<')
    formatString=formatString.replace('&gt;','>')
    return formatString

def returnModified(fileName):
    secs = os.path.getmtime(fileName)
    t = time.gmtime(secs)
    last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t)
    return last_mod_time

#create a TCP socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print('The server is ready to receive on port: ' + str(serverPort))
last_mod_time1=''

#loop forever listening for incoming TCP messages
while True:
    #receive client data
    ResponseData=''
    connectionSocket, address = serverSocket.accept()
    RequestData = connectionSocket.recv(1000000).decode()
    t = datetime.datetime.utcnow()
    RequestDateTime = t.strftime("%a, %d %b %Y %H:%M:%S GMT")
    print("Received Request")
    RequestLineCount=0
    for Line in RequestData.split("\r\n"):
        RequestLineCount+=1
    if RequestLineCount==5:
        for Line in RequestData.split("\r\n"):
            if "If-Modified-Since" in Line:
                last_mod_time1 = Line[19:]
                f = open(cache,"w")
                t= time.gmtime()
                lasttime = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t)
                f.write("Last-Modified: " + last_modified_current)
                f.close()
                #write to cache after conditional GET request where they is no cache present
    else:
        last_mod_time1=''
        
    for item in RequestData.split():
        if item[0] == "/":
            filename = item[1:]
            break
 
    if not(os.path.isfile(filename)):
        ResponseData += "HTTP/1.1 404 Not Found" + "\r\n"
        ResponseData += "Date: " + RequestDateTime + "\r\n"
        ResponseData += "\r\n"
    else:
        last_modified_current = returnModified(filename)
        if last_modified_current == last_mod_time1:
            ResponseData += "HTTP/1.1 304 Not Modified\r\n"
            ResponseData += "Date: " + RequestDateTime + "\r\n"
            ResponseData += "\r\n"
        else:
            ContentData = returnContent(filename)
            ContentLength = str(len(ContentData))
            ResponseData += "HTTP/1.1 200 OK" + "\r\n"
            ResponseData += "Date: " + RequestDateTime  + "\r\n"
            ResponseData += "Last-Modified: " + last_modified_current + "\r\n"
            ResponseData += "Content-Length: " + ContentLength + "\r\n"
            ResponseData += "Content-Type: text/html; charset=UTF-8" + "\r\n"
            ResponseData += "\r\n" + ContentData
    connectionSocket.send(ResponseData.encode())
    print("Sending Response")

    connectionSocket.close()
