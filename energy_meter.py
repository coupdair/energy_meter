#!/usr/bin/python

version='v0.0.2d'

#TODO:
## - bigger font size
## - fake head (using factory: fake, Gentec: old,new1,new2)

#NOTES:
## - power at 18mW, scale +18mW [0.00..0.10] mW axis range

#serial
import serial
#log
import string
import time
#graph
import numpy
import pylab as pl

serialDev='/dev/ttyUSB0'

ser = serial.Serial(serialDev, 57600, timeout=1)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)


#todo
frequency=10 #Hz
name='energy'
units='mJ'

#if frequency=0 then power, W
#name='power'
#units='mW'



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
ser.write("*F02");
line = ser.readline()
line = ser.readline()
print("*F02=|"+line+"|")
device_info=line.split("\t")

for i in range(0,len(device_info)-1,2):
  print('device_info['+str(i)+']('+device_info[i]+')='+device_info[i+1])+' ['+str(i+1)+']'

def get_wavelength_str():
    #many information
    ser.write("*F01");
    line = ser.readline()
    line = ser.readline()
    device_info=line.split("\t")
    #single one
    device_wavelength=device_info[4]+'='+device_info[5]+" nm"
    return device_wavelength;

device_wavelength=get_wavelength_str()

ser.write("*NAM");
line = ser.readline()
print("*NAM=|"+line+"|")
device_head=line

#plot data
data=numpy.empty(32)
data.fill(numpy.NAN)
i=data.size
##setup GUI window
pl.ion()
fig = pl.gcf()
fig.canvas.set_window_title('Power meter ('+'Gentec-Plink='+device_head+')')

#data recording
print '#date (date time),\t',name,'(',units,')'
checkWL=0
checkWL_size=5
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
  #convert to float
  val=float(line)*1000/frequency
  #convert to string, i.e. line
  strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
  strData=strTime+",\t" +str(val)
  #show
  print strData
  #write to file
  f = open("log_GentecPlink.txt","a")
  f.write(strData);f.write("\n")
  f.close()
  #plot data
  ##check boundary
  if(i<0):
    i=1
  i-=1
  ##shift previous values
  for j in range(i+1,data.size-1):
#    print(j+1)
    data[j]=data[j+1]
  ##set current value
  data[data.size-1]=val
  ##layout
  pl.clf()
  pl.title(time.strftime('%Hh%Mmin%Ss', current_time)+'\n'+device_wavelength+', current value='+str(round(val,4))+' '+units)
  pl.ylabel('\n'+name+' ('+units+')')
  pl.xlim([0,data.size])
  pl.xlabel('elapsed time (s)')
  pl.xticks([1,11,21,26,30,31], [30,20,10,5,1,0])
  ##plot
  pl.plot(data)
  pl.draw()
  ##get wavelength in case of setup change
  if(checkWL>checkWL_size):
    device_wavelength=get_wavelength_str()
    checkWL=0
  else:
    checkWL+=1
  #wait a while
  time.sleep(0.2)


