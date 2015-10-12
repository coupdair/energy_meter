#!/usr/bin/python

version='v0.0.3d'

#TODO:
## - other wavelength correction (table)

#log
import string
import time
#CLI argument
import argparse

#log setup parameter in a file
def log(set):
  current_time = time.localtime()
  strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
  strData=strTime+",\t" +set
  #write to file
  f = open("setup_GentecPlink.txt","a")
  f.write(strData);#f.write("\n")
  f.close()

#serial
import serial
#GUI
from Tkinter import *

#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--device",    help="device path (e.g. /dev/ttyUSB0)", default='/dev/ttyUSB0')
args = parser.parse_args()

serialDev=args.device #'/dev/ttyUSB0'

#device
ser = serial.Serial(serialDev, 57600, timeout=1)

#GUI
root = Tk()
root.title("setup wavelength, anticipation and zero offset")

#device
print '\nshow serial information:\n'
##Plink version
ser.write("*VER");
line = ser.readline()
print("*VER=|"+line+"|")
log('open USB-Plink '+line)
##power head name
ser.write("*NAM");
line = ser.readline()
print("*NAM=|"+line+"|")
device_head=line
log('with head '+device_head)

def set_zero():
    ser.write("*SOU");

def set_wavelength(value):
    strValue='{:05d}'.format(value)
    print "set "+strValue+" nm."
    ser.write("*PWC"+strValue);
    line = ser.readline()
    print("*PWC"+strValue+"=|"+line+"|")
    if(line!="ACK\n"):
        print("Warning: no acknowledgement received (e.g. ACK!="+line+").?")

def get_wavelength():
    #many information
    ser.write("*F01");
    line = ser.readline()
    line = ser.readline()
#    print("*F01=|"+line+"|")
    device_info=line.split("\t")
    
#    for i in range(0,len(device_info)-1,2):
#      print('device_info['+str(i)+']('+device_info[i]+')='+device_info[i+1])+' ['+str(i+1)+']'
    
#    print('dev.'+device_info[4]+'='+device_info[5])
    device_wavelength=int(device_info[5])
#    print "get "+str(device_wavelength)+" nm."
    return device_wavelength;

def set_device(key):
    ser.write(key);
    line = ser.readline()
    print(key+"=|"+line+"|")

def get_anticipation():
    #many information
    ser.write("*F02");
    line = ser.readline()
    line = ser.readline()
    device_info=line.split("\t")
    device_anticipation=int(device_info[25])
    return device_anticipation;

def get_anticipation_GUI():
    if(get_anticipation()==1):
      bAntON["relief"]=SUNKEN;
      bAntOFF["relief"]=RAISED;
    else:
      bAntOFF["relief"]=SUNKEN;
      bAntON["relief"]=RAISED;

#GUI
##WaveLength
def callback(value, index):
    print "setting "+str(value)+" nm ..."
    set_wavelength(value)
    check=get_wavelength()
    print 'current='+str(check)+" nm."
    if(check!=value):
        print("Warning: "+str(value)+" nm not set ! (presently "+str(check)+"!="+str(value)+").?")
    #log setup change
    log("set wavelength correction to "+str(check)+" nm.\n")
    #update GUI
    for i in range(0,len(bWL)):
      bWL[i]["relief"]=RAISED
    bWL[index]["relief"]=SUNKEN

def callback1064():
    callback(1064,0)

def callback632():
    callback(632,1)

def callback532():
    callback(532,1)

def callback308():
    callback(308,2)

def callback266():
    callback(266,3)

##Anticipation ON/OFF
def callbackAnticipationON():
    print "anticipation ON ..."
    set_device("*ANT")
    get_anticipation_GUI()
    #log setup change
    log("set anticipation.\n")

def callbackAnticipationOFF():
    print "anticipation OFF ..."
    set_device("*ANF")
    get_anticipation_GUI()
    #log setup change
    log("set no anticipation.\n")

##set zero offset
def callbackZero():
    print "set zero offset."
    set_zero()
    #log setup change
    log("set zero offset.\n")

#create a toolbar
toolbar = Frame(root)
##WaveLength
bWL=[]
bWL.append(Button(toolbar, text="1064 nm",width=6, command=callback1064))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bWL.append(Button(toolbar, text="632 nm", width=6, command=callback632))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bWL.append(Button(toolbar, text="532 nm", width=6, command=callback532))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bWL.append(Button(toolbar, text="308 nm", width=6, command=callback308))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bWL.append(Button(toolbar, text="266 nm", width=6, command=callback266))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)
##Anticipation ON/OFF
bAntON=Button(toolbar, text="ON",  width=6, command=callbackAnticipationON)
bAntON.pack(side=LEFT, padx=2, pady=2)
bAntOFF=Button(toolbar, text="OFF", width=6, command=callbackAnticipationOFF)
bAntOFF.pack(side=LEFT, padx=2, pady=2)

bMisc=[]
bMisc=Button(toolbar, text="zero",  width=6, command=callbackZero)
bMisc.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

get_anticipation_GUI()

line = ser.readline()

#tick (GUI)
clock = Label(font=("Helvetica", 16))
clock.pack()

def tick():
  #get time
  curtime=time.strftime('%Hh %Mmin %Ss')
  #get value
  ser.write("*CVU");
  ##line = "123.456"
  line = ser.readline()
  line = ser.readline()
  print("*CVU=|"+line+"|\n")
  print(len(line))
  if(len(line)<7):
    print("Warning: bad value (e.g. ACK) line="+line+"")
    val=-99
  else:
    val=float(line)
  clock.config(text=curtime+"      "+str(round(val,5)))
  clock.after(1000, tick)

tick()
root.mainloop()


