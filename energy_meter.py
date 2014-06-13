#!/usr/bin/python

import serial
import string
import time

serialDev='/dev/ttyUSB0'

ser = serial.Serial(serialDev, 57600, timeout=1)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

print 'record 1 value from ', serialDev
print 'format: date\tpower'
print 'example:'
line = "123.456"
val=float(line)
current_time = time.localtime()
strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
strData=strTime+",\t" +str(val)
print strData

print '\nshow serial information:\n'
#Plink version
ser.write("*VER");
line = ser.readline()
print("*VER=|"+line+"|")
#many information
ser.write("*F01");
line = ser.readline()
line = ser.readline()
print("*F01=|"+line+"|")

print '#date (date time),\tpower (W)'
#for i in range(0,3):
while(True):
  #ask and get data
  ser.write("*CVU");
  ##line = "123.456"
  line = ser.readline()
  line = ser.readline()
###  print("*CVU=|"+line+"|\n")
  #get time
  current_time = time.localtime()
  #convert to integer
  val=float(line)
  #convert to string, i.e. line
  strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
  strData=strTime+",\t" +str(val)
  #show
  print strData
  #write to file
  f = open("log_GentecPlink.txt","a")
  f.write(strData);f.write("\n")
  f.close()
  #wait a while
  time.sleep(1)


