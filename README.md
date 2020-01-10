______________ origin __________________

SwitchDoc Labs, LLC
June 2014

https://github.com/switchdoclabs/iBeacon-Scanner-

https://www.switchdoc.com/2014/08/ibeacon-raspberry-pi-scanner-python/
________________________________________

Editet January 2020, Daniel Lehmann, github@fototux.com
________________________________________

blescan.py is a python program designed to read iBeacon advertizments using a linux system. There might be a way to run python-bluez on Windows or MAC systems but this not covered.

The example "shtc3_beacon_scanner.py" shows how to use the scanner to receive data from the BLE beacon for temperature and relative humidity measurements https://github.com/Sensirion/shtc3_ble_beacon.

The example "AQ_Minion_beacon_scanner.py" could be used to read data from Sensirion's AQ Minion.

A generic scan could be done when executing the command "sudo python minimal_example.py"

The scripts have been tested on Ubuntu 18.04 and Raspbian. 

Required to install:
sudo apt-get install bluetooth bluez python-bluez python






