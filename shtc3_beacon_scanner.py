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

datafile = './measurement_data.csv'

file_t = '/var/www/html/sensor_web/t.txt'
file_rh = '/var/www/html/sensor_web/rh.txt' 
file_ah = '/var/www/html/sensor_web/ah.txt' 
file_dp = '/var/www/html/sensor_web/dp.txt'


# specific device uuid as defined in device firmware
uuid="1331ddee130629068283280700010001"

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
	
	fp_data = open(datafile,"a")
	fp_data.write('Epoch_UTC, MAC, T, RH, AH, DP')
	fp_data.close()
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
			t = int(beacon.split(',')[3])
			t = calculate_temperature(t)

			rh = int(beacon.split(',')[4])
			rh = calculate_humidity(rh)

			ah = calculate_absolute_humidity(t, rh)
			dp = calculate_dewpoint(t, rh)

			time_at = str(datetime.now())
			mac = beacon.split(',')[0]

			print ('{}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(time_at, mac, t, rh, ah, dp))

			fp_data = open(datafile,"a")
			fp_data.write('{}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(time_at, mac, t, rh, ah, dp))
			fp_data.close()

			f_t = open(file_t,"w+")
			f_rh = open(file_rh,"w+")
			f_ah = open(file_ah,"w+")
			f_dp = open(file_dp,"w+")
			
			f_t.write('{:.2f}'.format(t))
			f_rh.write('{:.2f}'.format(rh))
			f_ah.write('{:.2f}'.format(ah))
			f_dp.write('{:.2f}'.format(dp))			

			f_t.close()
			f_rh.close()
			f_ah.close()
			f_dp.close()
			
	time.sleep(5)
