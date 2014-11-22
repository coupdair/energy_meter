#log
import string
#serial
import serial

class energy_meter_device:
  """energy meter device template (base class)"""
  version='v0.0.1'
  __name='energy_meter_device'
  def __init__(self, serial_device):
    print self.__name+"::init(path)"
    self.serial_device_path=serial_device #'/dev/ttyUSB0'
    self.serial_device=0 #store serial.Serial object (e.g. self.serial_device=serial.Serial(serial_device_path, 57600, timeout=1) )
    self.device="empty" #energy meter device name (e.g. "Plink version")
    self.device_head="empty" #device head name that is connected to energy meter (e.g. "UP-1234")
    self.frequency=0 #0: power, >0: energy at nHz

  def open(self):
    print self.__name+"::open()"

  def set_mode(self,mode,frequency,log):
    print self.__name+"::set_mode(mode,frequency,log)"
    self.frequency=frequency
    if(mode=='power'):
      self.frequency=0 #Hz
    if (self.frequency>0):
      self.name='energy'
      self.units='mJ'
      log.log('configuration: '+self.name+' ('+self.units+') at '+str(self.frequency)+' Hz.\n')
    else: #frequency=0 then power, W
      self.name='power'
      self.units='mW'
      log.log('configuration: '+self.name+' ('+self.units+').\n')

  def information(self,log):
    print self.__name+"::information(log)"
    self.device_head='head: none as template class'
    log.log(self.device_head)

  def value(self):
    print self.__name+"::value()"

  def set_zero(self):
    print self.__name+"::set_zero()"

  def set_wavelength(self,value):
    print self.__name+"::set_wavelength(value)"

  def get_wavelength(self):
    print self.__name+"::get_wavelength()"

  def get_wavelength_str(self):
    print self.__name+"::get_wavelength_str()"

  def get_anticipation(self):
    print self.__name+"::get_anticipation()"
    return -1;

  def set_anticipation_ON(self):
    print self.__name+"::set_anticipation_ON()"

  def set_anticipation_OFF(self):
    print self.__name+"::set_anticipation_OFF()"


class energy_meter_file(energy_meter_device):
  """energy meter device through file (fake)"""
  version='v0.0.0'
  __name='energy_meter_file'

  def open(self):
    print self.__name+"::open()"
    self.serial_device=open(self.serial_device_path)


class energy_meter_usblink(energy_meter_device):
  """energy meter device through serial device"""
  version='v0.0.1'
  __name='energy_meter_usblink'

  def open(self):
    print self.__name+"::open()"
    self.serial_device=serial.Serial(self.serial_device_path, 57600, timeout=1) #create and open device as a Serial object

  def set_device(self,key):
    print self.__name+"::set_device(key)"
    self.serial_device.write(key);
    line = self.serial_device.readline()

  def information(self,log):
    print self.__name+"::information(log)"
    print '\nshow serial information:\n'
    log.log('serial path: '+self.serial_device_path)
    ##Plink version
#todo or not: use self.set_device("*VER")
    self.serial_device.write("*VER");
    line = self.serial_device.readline()
    #print("*VER=|"+line+"|")
    log.log('device USB-Plink '+line)
    ##power head name
#todo or not: use self.set_device("*NAM")
    self.serial_device.write("*NAM");
    line=self.serial_device.readline()
    #print("*NAM=|"+line+"|")
    self.device_head=line
    log.log('with head '+self.device_head)

  def value(self):
    print self.__name+"::value()"
    #ask and get data
    self.set_device("*CVU")
    ##line = "123.456"
    line = self.serial_device.readline()
    #print("*CVU=|"+line+"|\n")
    if (self.frequency>0):
      val=float(line)*1000/self.frequency #mJ
    else:
      val=float(line)*1000 #mW
    return val

  def set_zero(self):
    print self.__name+"::set_zero()"
    self.set_device("*SOU");
    line = self.serial_device.readline()
    line = self.serial_device.readline()
    line = self.serial_device.readline()

  def set_wavelength(self,value):
    print self.__name+"::set_wavelength(value)"
    strValue='{:05d}'.format(value)
    print "set "+strValue+" nm."
#todo or not: use self.set_device("*PWC"+strValue)
    self.serial_device.write("*PWC"+strValue);
    line = self.serial_device.readline()
    #print("*PWC"+strValue+"=|"+line+"|")
    line=line.replace('\n','').replace('\r','')
    if(line!="ACK"):
      print("Warning: no acknowledgement received (e.g. ACK!="+line+").?")

  def get_wavelength(self):
    print self.__name+"::get_wavelength()"
    #many information
#todo: use self.set_device("*F01")
    self.set_device("*F01")
    line = self.serial_device.readline()
#    print("*F01=|"+line+"|")
    device_info=line.split("\t")
    
#    for i in range(0,len(device_info)-1,2):
#      print('device_info['+str(i)+']('+device_info[i]+')='+device_info[i+1])+' ['+str(i+1)+']'
    
#    print('dev.'+device_info[4]+'='+device_info[5])
    device_wavelength=int(device_info[5])
#    print "get "+str(device_wavelength)+" nm."
    return device_wavelength;

  def get_wavelength_str(self):
    print self.__name+"::get_wavelength_str()"
    #many information
    self.set_device("*F01");
    line = ser.readline()
    device_info=line.split("\t")
    #single one
    device_wavelength=device_info[4]+'='+device_info[5]+" nm"
    return device_wavelength;

  def get_anticipation(self):
    print self.__name+"::get_anticipation()"
    #many information
#todo: use self.set_device("*F02")
    self.serial_device.write("*F02");
    line = self.serial_device.readline()
    line = self.serial_device.readline()
    device_info=line.split("\t")
    device_anticipation=int(device_info[25])
    return device_anticipation;

  def set_anticipation_ON(self):
    print self.__name+"::set_anticipation_ON()"
    self.set_device("*ANT")

  def set_anticipation_OFF(self):
    print self.__name+"::set_anticipation_OFF()"
    self.set_device("*ANF")

#energy_meter_device
