#!/usr/bin/python

version='v0.2.0'

#user needs:
# - tty access:
#   $sudo adduser $USER dialout

#TODO:
## v pause
## v .median( (or .mean() ), CLOption for size
## _ zero in graph with red lines
## . time elasped: v30s, 1, 2, 3, 4 and v5min
## . fake head (using factory: fake, Gentec: old,new1,new2)
## o merge meter and setup (due to serial dialog errors, if separated process)

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
#CLI argument
import argparse

#GUI
from Tkinter import *

#GUI
root = Tk()
root.title("duration")

#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--device",    help="device path (e.g. /dev/ttyUSB0)", default='/dev/ttyUSB0')
parser.add_argument("--mode",      help="device path (e.g. power or energy)", default='power')
parser.add_argument("--frequency", help="laser frequency (e.g. 10 Hz)", default=10, type=int)
parser.add_argument("--duration",  help="graph duration (e.g. 5 for 5min)", default=5, type=int)
parser.add_argument('-s',"--stat-run-average-size", help="running average size (e.g. mean on 16 samples)", default=16, type=int)
args = parser.parse_args()

serialDev=args.device #'/dev/ttyUSB0'

ser = serial.Serial(serialDev, 57600, timeout=1)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

#log setup parameter in a file
def log(set):
  current_time = time.localtime()
  strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
  strData=strTime+",\t" +set
  #write to file
  f = open("setup_GentecPlink.txt","a")
  f.write(strData);#f.write("\n")
  f.close()

#power or energy
#todo: use nrj.mode(args.mode,args.frequency,log)
frequency=args.frequency
if(args.mode=='power'):
  frequency=0 #Hz
if (frequency>0):
  name='energy'
  units='mJ'
  log('configuration: '+name+' ('+units+') at '+str(frequency)+' Hz.\n')
else: #frequency=0 then power, W
  name='power'
  units='mW'
  log('configuration: '+name+' ('+units+').\n')


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

def set_zero():
    ser.write("*SOU");
    #dummy read for ACK or any else
    line = ser.readline()#dummy read for ACK or any else
    print '/' #,end='\r')
    line = ser.readline()#dummy read for ACK or any else
    print('-')#,end='\r')
    line = ser.readline()#dummy read for ACK or any else
    print('\\')#,end='\r')
    line = ser.readline()#dummy read for ACK or any else
    print('|')#,end='\r')
    #wait for stabilisation
    time.sleep(1)
    print('/')#,end='\r')
    time.sleep(1)
    print('-')#,end='\r')
    time.sleep(1)
    print('\\')#,end='\r')
    #skip 5 dummy values
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
    print("*CVU=|"+line+"|\n")

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
tmp=line.split("\n")
tmp=tmp[0]
device_head=tmp.replace("\t\r\r","")

#plot data
duration=args.duration #30
data=numpy.empty(5*60+2) #data size 5min
if (duration==5):
  data_dur=numpy.empty(5*60+2) #data size 5min
else:
  data_dur=numpy.empty(32) #data size 30s

##statistics
run_avg_size=args.stat_run_average_size #running average size (from command line or default)
run_avg=numpy.empty(data.size) #running average data
run_avg_limit=numpy.empty(data.size) #running average data

##pause
pause=numpy.empty(data.size) #pause position

##init data: fill with NaN for graph
data.fill(numpy.NAN)
data_dur.fill(numpy.NAN)
run_avg.fill(numpy.NAN)
run_avg_limit.fill(numpy.NAN)
pause.fill(numpy.NAN)
run_avg_limit_i=data.size-run_avg_size
run_avg_limit[run_avg_limit_i]=-1; run_avg_limit[run_avg_limit_i+1]=1;
i=data.size

##setup GUI window

pl.ion()
fig=pl.figure(figsize=(10,10))
fig.canvas.set_window_title('Power meter ('+'Gentec-Plink='+device_head+')')

#data recording
print '#device head name;date (date time);',name,'(',units,')'
checkWL=0
checkWL_size=5


#tick
bPause=False

def callback(value, index):
  global duration
  duration=value
  #update GUI
  for i in range(0,len(bWL)):
    bWL[i]["relief"]=RAISED
  bWL[index]["relief"]=SUNKEN

def callback30():
  callback(30,0)

def callback5():
  callback(5,1)

##set zero offset
def callbackZero():
    print "set zero offset."
    set_zero()
    #log setup change
    log("set zero offset.\n")

def callbackPause():
  global bPause
  global pause
  global data
  bPause=not bPause
  if(bPause):
    #pressed
    bTimeLine[0]["relief"]=SUNKEN
    #add pause in graph data
    pause[data.size-3]=numpy.nanmin(data)
    pause[data.size-2]=numpy.nanmax(data)
  else:
    #unpressed
    bTimeLine[0]["relief"]=RAISED

def callbackQuit():
  sys.exit(0)

#create a toolbar
toolbar = Frame(root)
##WaveLength
bWL=[]
bWL.append(Button(toolbar, text="30 s",width=6, command=callback30))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bWL.append(Button(toolbar, text="5 min", width=6, command=callback5))
bWL[len(bWL)-1].pack(side=LEFT, padx=2, pady=2)

bMisc=[]
bMisc=Button(toolbar, text="zero",  width=6, command=callbackZero)
bMisc.pack(side=LEFT, padx=2, pady=2)

bTimeLine=[]
bTimeLine.append(Button(toolbar, text="pause",width=6, command=callbackPause))
bTimeLine[len(bTimeLine)-1].pack(side=LEFT, padx=2, pady=2)

bTimeLine.append(Button(toolbar, text="quit",width=6, command=callbackQuit))
bTimeLine[len(bTimeLine)-1].pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

def tick():
  global i, device_wavelength, checkWL, data, data_dur, bPause

  if(not bPause):
    #ask and get data
    ser.write("*CVU");
    ##line = "123.456"
    line = ser.readline()
    line = ser.readline()
###    print("*CVU=|"+line+"|\n")
    #get time
    current_time = time.localtime()
    #convert to float
    if (frequency>0):
      val=float(line)*1000/frequency
    else:
      val=float(line)*1000
    #convert to string, i.e. line
    strTime=time.strftime('%d/%m/%Y %H:%M:%S', current_time)
    strData=device_head+";"+strTime+";"+str(val)
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
#      print(j+1)
      data[j]=data[j+1]
      run_avg[j]=run_avg[j+1]
      pause[j]=pause[j+1]
    ##set current value
    data[data.size-1]=val
    data_dur=data #[data.size-data_dur.size-2:data.size-1]
    #statistics
    run_avg[data.size-run_avg_size/2-1]=numpy.nanmean(data[data.size-run_avg_size-1:data.size-1]) #numpy.median, numpy.nanmean
    print(run_avg[data.size-run_avg_size/2-1])
    run_avg_limit[run_avg_limit_i]=numpy.nanmin(data); run_avg_limit[run_avg_limit_i+1]=numpy.nanmax(data);
  ##layout
  pl.clf()
  fontsize='xx-large'
  if(not bPause):
    title=time.strftime('%Hh%Mmin%Ss', current_time)
  else:
    title='pause'
    val=data[data.size-1]
  pl.title(title+'\n'+device_wavelength+', current value='+str(round(val,4))+' '+units+', mean='+str(round(run_avg[data.size-run_avg_size/2-1],4))+' '+units, fontsize=fontsize)
  pl.ylabel('\n'+name+' ('+units+')')
  pl.yticks(fontsize=fontsize)
  pl.xlim([0,data.size])
  if (duration==5):
    pl.xlabel('elapsed time (min)')
    pl.xticks([1,61,2*60+1,3*60+1,4*60+1,4*60+31,5*60+1], [5,4,3,2,1,0.5,0]) #5min
  else:
    pl.xlabel('elapsed time (s)')
    pl.xticks([1,11,21,26,30,31], [30,20,10,5,1,0]) #30s
  ##plot
  pl.plot(data_dur, linewidth=3.21)
  pl.plot(run_avg)
  pl.plot(run_avg_limit)
  pl.draw()
  ##get wavelength in case of setup change
  if(checkWL>checkWL_size):
    device_wavelength=get_wavelength_str()
    checkWL=0
  else:
    checkWL+=1
  #wait a while
  bWL[0].after(567, tick)
#  bWL[0].after(1000, tick)

tick()
root.mainloop()
