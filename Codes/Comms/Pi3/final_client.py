from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime
import socket
import base64
import random
import serial
import sys
import time
import array
import numpy as np
import pandas as df
from Brain import Brain
from sklearn.externals import joblib

debugLoops = 60
key = '3002300230023002'

class client:
    def __init__(self, ip_addr, port_num):
      self.key = "3002300230023002"
      print(str(datetime.now()))
      print("Initializing")
      #Create a TCP/IP socket
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_address = (ip_addr, port_num)
      print('Connecting to %s port %s' % server_address)
      self.sock.connect((ip_addr, port_num))
      self.actions = ['logout', 'wavehands', 'jump', 'frontback', 'turnclap', 'windowcleaning', 'numbersix', 'jumpleftright', 'sidestep', 'squadturnclap', 'window360']
      print('Connected to server')
      time.sleep(5)
    
    def sendEncoded(self, message):
      print(message)
      encrypted = self.encrypt(message)
      self.sock.send(encrypted)

    def encrypt(self, message):
      print("in encrypt :   ", message)
      BLOCK_SIZE = 16
      PADDING = ' '
      pad = lambda s: s + (BLOCK_SIZE - (len(s) % BLOCK_SIZE)) * PADDING
      IV = Random.new().read(AES.block_size)
      cipher = AES.new(key, AES.MODE_CBC, IV)
      paddedMessage = pad(message)
      encoded = base64.b64encode(IV + cipher.encrypt(paddedMessage))
      print (type(encoded))
      return encoded

    def getMessage(self, move, powerReading):
      message = ('#' + move + '|' + str(powerReading[0])+ '|' + str(powerReading[1]) + '|' + str(powerReading[2]) + '|' + str(powerReading[3]) + "|")
      print (message)
      return message

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Invalid number of arguments')
        print('python server.py [IP address] [Port]')
        sys.exit()

    ip_addr = sys.argv[1]
    port_num = int(sys.argv[2])
    my_client = client(ip_addr, port_num)

    rndforest = joblib.load('rdf_model.pkl')    
    checkHS = False
    ignoreLoopCount = 0
    debugFails = 0
    loopCount = 0
    successCount = 0
    checkSumFailCount = 0
    current_milli_time = lambda: int(round(time.time() * 1000))
    newFID = 0
    oldFID = 0
    hashcount = 0
    msgCheckSum = 0
    chkSum = 0
    prevPred = 0
    pred = 0
    hello = bytes('H', encoding = 'utf-8')
    ack = bytes('A', encoding = 'utf-8')
    sendData = bytes('D', encoding = 'utf-8') 
    
    try:
      #Connections  
      port = serial.Serial('/dev/serial0', baudrate=115200, timeout=0.1)
      print("Connecting to Arduino")
      port.flushInput() # Clear port
        
      while(checkHS == False):
        port.write(hello)
        print("H sent, awaiting response")
        time.sleep(0.5)
        reply = port.read().decode('utf-8')
        if(reply == 'A'):
          port.write(ack)
          reply2 = port.read().decode('utf-8')
          port.readline()
          if(reply2 == 'A'):
            checkHS = True
            port.reset_input_buffer()
            print("Connected to Arduino")
            port.readline()
            time.sleep(0.5)

          time.sleep(0.1)
        else:
          time.sleep(0.5)
        
      # Begin System Test
      print("Begin Systems Checks")
      time.sleep(0.5)
      startTime = loopTime = current_milli_time()
      print(startTime)
      port.readline() # Clear Port
      time.sleep(0.2)
      
      while(ignoreLoopCount < debugLoops):
        port.write(sendData)
        message = port.readline().decode('utf-8')
        readEndTime = current_milli_time()
        print("Count: ", ignoreLoopCount)
        print("Message: ", message)
    
        newFID = int(message.split(',',1)[0])
    
        msgCheckSum = int((message.rsplit(',', 1)[1])[:-2])
        message = message.rsplit(',', 1)[0]
        byteMessage = bytearray(message, 'utf-8')
          
        if(newFID == (oldFID + 1)): 
          oldFID = newFID
          while (hashcount < len(byteMessage)):
            chkSum ^= int(byteMessage[hashcount])
            hashcount += 1
          if (chkSum == msgCheckSum):
            print("Matching Checksums")
          else:
            debugFails += 1
            print("Checksum error!", "Message Checksum: ", msgCheckSum, "Generated Checksum: ", chkSum)
            print(' ')
          
        elif (newFID == oldFID):
          debugFails += 1
          print("Same message sent")
          print(" ")
        else:
          debugFails += 1
          print('ID Error', 'Old ID: ', oldFID, 'New ID: ', newFID)
          print(' ')
                    
        ignoreLoopCount += 1
        chkSum = 0
        hashcount = 0
        oldFID = newFID
        #print("Debug Loop: ", ignoreLoopCount, "Reading has taken: ", readEndTime - readTime, "ms", "Others have taken: ", current_milli_time()-readEndTime, "ms")
        time.sleep(0.4)
        

      count = -1
      end = 1
      time.sleep(22)
      print("System live")
      print(" ")
      print("Start sending moves to Server")
      time.sleep(0.5)
    
      while(end == 1) :
        powerReadings = []
        samplePoints = []
        loopTime = current_milli_time()
        
        while(loopCount < 50) :
          temp = []
          port.write(sendData)
          message = port.readline().decode('utf-8')
          #print(message)
          newFID = int(message.split(',',1)[0])
          msgCheckSum = int((message.rsplit(',', 1)[1])[:-2])
          message = message.rsplit(',', 1)[0]
          byteMessage = bytearray(message, 'utf-8')
          temp = message.split(',')
          
          if(newFID == (oldFID + 1)): 
            oldFID = newFID
            while (hashcount < len(byteMessage)):
              chkSum ^= int(byteMessage[hashcount])
              hashcount += 1
            if (chkSum != msgCheckSum):
              print("Checksum Error")

          elif (newFID == oldFID):
            print("Same message sent")
            print(" ")
          else:
            print('ID Error', 'Old ID: ', oldFID, 'New ID: ', newFID)
            print(' ')
            
          #print(float(temp[1]))
          for i in range (0,len(temp)):
            temp[i] = float(temp[i])
          #print temp
          powerReadings = temp[13:17]
          samplePoints.append((temp[1:13]))
          chkSum = 0
          oldFID = newFID
          hashcount = 0
          loopCount += 1

        #print samplePoints
        endlooptime = current_milli_time()
        #print ("Time of loop: ", endlooptime - loopTime)
        print (powerReadings)
        loopCount = 0
        confidence = 0
        pred,confidence = Brain(samplePoints,rndforest)
        varname = ['logout', 'wavehands', 'jump', 'frontback', 'turnclap', 'windowcleaning', 'numbersix', 'jumpleftright', 'sidestep', 'squatturnclap', 'windowcleaning360']
        if(confidence > 0.50) :
            if(count < 0) :
              print ("current value")
              print(varname[pred])
              if(pred == prevPred):
                count += 1
              else:   
                count = -1
              print(count)
            else:
              if(pred == prevPred):
                print("Prediction to server")
                print (varname[pred]) #send to server confirmed.
                count = -1
                send_message = my_client.getMessage(varname[pred], powerReadings)
                my_client.sendEncoded(send_message)
                time.sleep(1.5)
                if(pred == 0):
                  end = 0
                  print (varname[pred]) #send to server confirmed.
                  send_message = my_client.getMessage(varname[pred], powerReadings)
                  my_client.sendEncoded(send_message)
                  endTime = current_milli_time() - startTime
                  print ("Total time run: ", endTime)
              else:
                count = -1
                print(count)

            prevPred = pred
              
    except KeyboardInterrupt:
      sys.exit(1)
      
