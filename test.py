#!/usr/bin/python

#serial
import time
#CLI argument
import argparse

import energy_meter_device

#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--device",    help="device path (e.g. /dev/ttyUSB0)", default='/dev/ttyUSB0')
args = parser.parse_args()

ser=energy_meter_device.energy_meter_device(args.device) #'/dev/ttyUSB0'

print "energy_meter_device version=", ser.version
print "path=", ser.serial_device_path
