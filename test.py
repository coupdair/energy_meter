#!/usr/bin/python

#serial
import time
#CLI argument
import argparse

import energy_meter_device
import logger

#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--device",    help="device path (e.g. /dev/ttyUSB0)", default='/dev/ttyUSB0')
args = parser.parse_args()

nrj=energy_meter_device.energy_meter_device(args.device) #'/dev/ttyUSB0'
#nrj=energy_meter_device.energy_meter_usblink(args.device) #'/dev/ttyUSB0'
log=logger.logger("log_test.txt")#"setup_GentecPlink.txt")

print "energy_meter_device version=", nrj.version
print "path=", nrj.serial_device_path

log.log(nrj.serial_device_path+" open")

#print('open')
#nrj.open()

nrj.set_mode('power',0,log)
nrj.information(log)
nrj.set_anticipation_ON()
nrj.set_anticipation_OFF()

