#Nikhil Ramesh
#31499350
#Section 02
#! /usr/bin/env python3
# HTTP Client
import sys
import socket
import time
import struct
import os, os.path
import datetime, time
import codecs

#localhost:12000/filename.html
#127.0.0.1:12000/filename.html
data = sys.argv[1]
host, rawData = data.split(":")
port, filename = rawData.split("/")
port = int(port)
cache = 'cache.txt'
#HTTP GetRequest based on HTTP formatting
getRequest = "GET /" + filename + " HTTP/1.1" + "\r\n"
getRequest += host + ":" + str(port) + "\r\n"
getRequest += "\r\n"

#TCP clientSocket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))
clientSocket.send(getRequest.encode())
print("\nHTTP GET Request")

# Receive the server response
getResponse = clientSocket.recv(4096)
getResponse = getResponse.decode()

if "HTTP/1.1 404" in getResponse:
    #HTTP/1.1 404 (404 code page does not exist)
    print(getResponse)
    clientSocket.close()
else:
    print(getResponse+"\n")
    clientSocket.close()

    # = "cache.txt"
    lastmodified = ""
    if os.path.isfile(cache):
        f = open(cache,"r")
        lines = f.readlines()
        #parse thru cache for Last-Modified tag and store in lastmodified
        for line in lines:
            if "Last-Modified" in line:
                lastmodified=line[15:]
        f.close()
    else:
        t = time.gmtime(0)
        lasttime = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t)
        lastmodified = lasttime

    #conditional getRequest
    getRequest = "GET /"+ filename +" HTTP/1.1" + "\r\n"
    getRequest += host+":"+str(port)+"\r\n"
    getRequest +="If-Modified-Since: " + lastmodified + "\r\n"
    getRequest += "\r\n"
    
    print("\nHTTP Conditional GET Request")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    clientSocket.send(getRequest.encode())
    ResponseData = clientSocket.recv(4096)
    ResponseData = ResponseData.decode()
    print(ResponseData)
    clientSocket.close()
