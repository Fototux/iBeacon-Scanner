# ------------ origin ------------------
# https://github.com/switchdoclabs/iBeacon-Scanner-
# https://www.switchdoc.com/2014/08/ibeacon-raspberry-pi-scanner-python/
# --------------------------------------

import blescan

import sys
import bluetooth._bluetooth as bluez

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
		print (beacon)
	time.sleep(5)

