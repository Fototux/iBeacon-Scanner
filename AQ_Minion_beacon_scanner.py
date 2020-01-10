# ------------ origin ------------------
# https://github.com/switchdoclabs/iBeacon-Scanner-
# https://www.switchdoc.com/2014/08/ibeacon-raspberry-pi-scanner-python/
# --------------------------------------

import blescan

import sys
import bluetooth._bluetooth as bluez

import time
from datetime import datetime

import math

# specific device uuid as defined in device firmware
uuid="d5060003"

def calculate_temperature(temperature):
	return ((temperature / 65536.) * 175. - 45)

def calculate_humidity(humidity):
	return ((humidity / 65536.) * 100.)

def calculate_absolute_humidity(temperature, humidity):
	# Calculates the absolute humidity (g/m^3) from %RH and T (Celsius)
	return 216.7 * humidity / 100. * 6.112 * math.exp(17.62 * temperature / (243.12 + temperature)) / (273.15 + temperature)

def calculate_dewpoint(temperature, humidity):
	# Calculates the dew point (Celsius) from %RH and T (Celsius)
	dewpoint = (math.log10(humidity) - 2) / 0.4343 + (17.62*temperature)/(243.12+temperature);
	return 243.12 * dewpoint / (17.62 - dewpoint)

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print ('ble thread started')
	print ('Epoch_UTC, MAC, T, RH, AH, DP')

except:
	print ('error accessing bluetooth device...')
	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
		if uuid in beacon:
			t_lsb = beacon.split(',')[2][4:6]
			t_msb = beacon.split(',')[2][6:8]
			t = calculate_temperature(int(t_msb + t_lsb,16))

			rh_lsb = beacon.split(',')[2][8:10]
			rh_msb = beacon.split(',')[2][10:12]
			rh = calculate_humidity(int(rh_msb + rh_lsb,16))

			ah = calculate_absolute_humidity(t, rh)
			dp = calculate_dewpoint(t, rh)

			time_at = str(datetime.now())
			mac = beacon.split(',')[0]

			print ('{}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(time_at, mac, t, rh, ah, dp))
	time.sleep(5)
