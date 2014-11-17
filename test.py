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
log=logger.logger("log_test.txt")#"setup_GentecPlink.txt")

print "energy_meter_device version=", nrj.version
print "path=", nrj.serial_device_path

log.log(nrj.serial_device_path+" open")

print('open')
nrj.open()

print('info')
nrj.information(log)

#test many functions
wavelength=nrj.get_wavelength()
print "wave lenght=", wavelength , " nm."
#nrj.value()
nrj.set_zero()
#nrj.value()
nrj.set_wavelength(532)
anticipation=nrj.get_anticipation(); print "anticipation=", anticipation
nrj.set_anticipation_ON()
anticipation=nrj.get_anticipation(); print "anticipation=", anticipation
nrj.set_anticipation_OFF()
anticipation=nrj.get_anticipation(); print "anticipation=", anticipation

