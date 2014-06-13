#!/usr/bin/python

#serial
import serial
#GUI
from Tkinter import *

#device
serialDev='/dev/ttyUSB0'
ser = serial.Serial(serialDev, 57600, timeout=1)

#GUI
root = Tk()
root.title("setup wavelength")

#device
print '\nshow serial information:\n'
#Plink version
ser.write("*VER");
line = ser.readline()
print("*VER=|"+line+"|")

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
    device_wavelength=device_info[5]
#    print "get "+str(device_wavelength)+" nm."
    return device_wavelength;

#GUI
def callback(value):
    print "setting "+str(value)+" nm ..."
    set_wavelength(value)
    check=get_wavelength()
    print 'current='+str(check)+" nm."
    if(check!=value):
        print("Warning: "+str(value)+" nm not set ! (presently "+str(check)+"!="+str(value)+").?")

def callback1064():
    callback(1064)

def callback532():
    callback(532)

def callback266():
    callback(266)

# create a toolbar
toolbar = Frame(root)

b = Button(toolbar, text="1064 nm",width=6, command=callback1064)
b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="532 nm", width=6, command=callback532)
b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="266 nm", width=6, command=callback266)
b.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

root.mainloop()

#Example : *PWC01064 selects the wavelength 1064 nm

