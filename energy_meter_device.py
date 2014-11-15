#log
import string
#serial
import serial

class energy_meter_device:
  """energy meter device through serial device"""
  version='v0.0.0'
  def __init__(self, serial_device):
    self.serial_device_path=serial_device #'/dev/ttyUSB0'
    self.serial_device=0 #store serial.Serial object (e.g. self.serial_device=serial.Serial(serial_device_path, 57600, timeout=1) )
    self.device="empty" #energy meter device name (e.g. "Plink version")
    self.device_head="empty" #device head name that is connected to energy meter (e.g. "UP-1234")

  def open(self):
    self.serial_device=serial.Serial(serial_device_path, 57600, timeout=1) #create and open device as a Serial object

  def set_device(key):
    self.serial_device.write(key);
    line = self.serial_device.readline()
    print(key+"=|"+line+"|")

  def information(self):
    print '\nshow serial information:\n'
    ##Plink version
    self.serial_device.write("*VER");
    line = self.serial_device.readline()
    print("*VER=|"+line+"|")
    log('open USB-Plink '+line)
    ##power head name
    self.serial_device.write("*NAM");
    line=self.serial_device.readline()
    print("*NAM=|"+line+"|")
    self.device_head=line
    log('with head '+device_head)

  def set_zero():
    self.serial_device.write("*SOU");

  def set_wavelength(value):
    strValue='{:05d}'.format(value)
    print "set "+strValue+" nm."
    self.serial_device.write("*PWC"+strValue);
    line = self.serial_device.readline()
    print("*PWC"+strValue+"=|"+line+"|")
    if(line!="ACK\n"):
      print("Warning: no acknowledgement received (e.g. ACK!="+line+").?")

  def get_wavelength():
    #many information
    self.serial_device.write("*F01");
    line = self.serial_device.readline()
    line = self.serial_device.readline()
#    print("*F01=|"+line+"|")
    device_info=line.split("\t")
    
#    for i in range(0,len(device_info)-1,2):
#      print('device_info['+str(i)+']('+device_info[i]+')='+device_info[i+1])+' ['+str(i+1)+']'
    
#    print('dev.'+device_info[4]+'='+device_info[5])
    device_wavelength=int(device_info[5])
#    print "get "+str(device_wavelength)+" nm."
    return device_wavelength;

  def get_anticipation():
    #many information
    self.serial_device.write("*F02");
    line = self.serial_device.readline()
    line = self.serial_device.readline()
    device_info=line.split("\t")
    device_anticipation=int(device_info[25])
    return device_anticipation;
