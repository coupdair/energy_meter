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
    print "set "+str(value)+" nm."
#    ser.write("*PWC01064");
    ser.write("*PWC00532");
    line = ser.readline()
    print("*PWC01064=|"+line+"|")
    if(line!="ACK\n"):
        print("Warning: no acknowledgement received (e.g. ACK).")

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
def callback1064():
    print "called the callback 1064"
    set_wavelength(1064)
    print 'current='+str(get_wavelength())+" nm."

def callback532():
    print "called the callback 532"
    set_wavelength(532)
    print 'current='+str(get_wavelength())+" nm."

# create a toolbar
toolbar = Frame(root)

b = Button(toolbar, text="1064 nm", width=6, command=callback1064)
b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="532 nm", width=6, command=callback532)
b.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

root.mainloop()

#Example : *PWC01064 selects the wavelength 1064 nm

