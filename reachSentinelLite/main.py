'''
DO NOT DELETE:
exec(open("main.py").read()) --> to run this program from shell
'''

import time
import datetime
import serial
import socket
import math
import numpy as np
import os
import django

from gps.GPS import GPSInit, saveCoor, processCoordinates, calcVelGPS
from communication.sendUDP import initSocket, sendPacket, killSocket
from altimeter.altitudeCalculation import altitudeCalc
import acceleration
#from accel import findInertialFrameAccel

from graphs.models import Telemetry, IsLive, TimeInit  # exec(open("main.py").read())
##Initiate variables
FIRST = True

lat2 = 0
lon2 = 0
GPSInit()
velocity = np.matrix([0,0,0]).T
position = np.matrix([0,0,0]).T

#TODO function for dynamicaly assessing calibration constants
ACCX_CALIB = 0
ACCY_CALIB = 0
ACCZ_CALIB = 0

#set positions of data in incoming csv packet
TIMESTAMP = 0
ACCELX = 1
ACCELY = 2
ACCELZ = 3
GYROX = 4
GYROY = 5
GYROZ = 6
GPS_LAT = 7
GPS_LONG = 8
GPS_ALT = 9
GPS_HR = 10
GPS_MIN = 11
GPS_SEC = 12
TEMP = 13
PRESSURE = 14
ALTITUDE = 15
BARO_TEMP = 16

'''
MAGX = 7
MAGY = 8
MAGZ = 9
MAGHEAD = 10
TEMP = 11
PRESSURE = 13
ALTITUDE = 12
BAROTEMP = 14
'''

tots_not_launch = 1
count = 0

# --------------------------------------------- * * * ---------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reachSentinelLite.settings')
django.setup()

print("\n\n\n")
print(
	'             ||---------------------------- * * * -------------------------\\\\\n'\
	'             ||   ______                    _____                           \\\\\n'\
	'       ######||   | ___ \           ()     /  ___|                           \\\\\n'\
	'  ###########||   | |_/ /_ __ _   _ _ _ __ \ `--. _ __   __  _  ___ ___       \\\\\n'\
	"#############||   | ___ \ '__| | | | | '_ \ `--. \ '_ \ / _\| |/ __/ _ \       \\\\\n"\
	'   ##########||   | |_/ / |  | |_| | | | | /\__/ / |_) | (_ | | (__| __/       //\n'\
	'        #####||   \____/|_|   \__,_|_|_| |_\____/| .__/ \__/|_|\___\___|      //\n'\
	'      #######||                                  | |                         //\n'\
	'             ||                                  |_|                        //\n'\
	'             ||---------------------------- * * * -------------------------//\n')

print("\n\n\n")
'''
new_data = Telemetry.objects.create(  # -------------- * * * -------------- SAVE TO DATABASE
timestamp='11-28-2017 00:19:06', 
accel_x   = 8, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 74)
new_data.save()
'''


# Dabatase checks
if TimeInit.objects.count() != 0:
	for elem in IsLive.objects.all():
		elem.delete()

TimeInit.objects.create()

if Telemetry.objects.count() != 0:
	for elem in Telemetry.objects.all():
		elem.delete()

if Telemetry.objects.count() == 0:
	Telemetry.objects.create() # zero data-point

if IsLive.objects.count() != 0:  # ------------------ * * * ------------------ REQUIRES TESTING
	for elem in IsLive.objects.all():
		elem.delete()

downlink = IsLive.objects.create() # ----------------- * * * ----------------- INITIALLY FALSE, ON BUTTON-CLICK IN DASH, TRUE

try:
	print("Opening Serial Port...")
	#initiate serial port to read data from
	SERIAL_PORT = '/dev/cu.usbmodem14311'  # '/dev/cu.usbmodem14321'
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=9600,
	    timeout=3,                         # give up reading after 3 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print("connected to port " + SERIAL_PORT)
except:
	print("<== Error connecting to " + SERIAL_PORT + " ==>")
	exit()

##create plain text file to save raw data as backup for database
date = str(datetime.datetime.now())
FILENAME = 'Raw_Data/' + date
FILENAME = FILENAME.replace(':', '_')
txtfile = open(FILENAME, "w")
txtfile.write('Project Reach Raw Data starting at ' + date)

isFirst = True

##Main Processing Loop
while ser.isOpen():
	#get data
	dataString = str(ser.readline())
	print('Received: ' + dataString)
	txtfile.write(dataString)
	dataString = dataString[2:len(dataString)-5]
	print('Received: ' + dataString)

	'''
	LAST YEAR'S ORDER LEFT FOR REFERENCE, IS NOT USED
	parse string 
	create array with elements deliminated by spaces
	contents should be as follows
	data[0] = timestamp
	data[1] = pressure
	data[2] = temperature
	data[3] = gyroX
	data[4] = gyroY
	data[5] = gyroZ
	data[6] = accelX
	data[7] = accelY
	data[8] = accelZ
	data[9] = gps Time
	data[10] = lon
	data[11] = lat
	data[12] = gpsAlt
	data[13] = speed
	data[14] = course
	'''
	data = dataString.split(",")
	# convert to integer from string then try printing
	'''
	for i in range(len(data)):
		if (data[i] == 'NAN'):
			data[i] = 0
	'''

	for i in range(len(data)):
		if "NAN" in data[i]:
			data[i] = 0.0
			continue
		data[i] = float(data[i])
		
	print(data)

	if (isFirst):
		TimeInit.objects.get().timeInit = datetime.datetime.now() - data[TIMESTAMP]
		isFirst = False




	print("Timestamp", data[TIMESTAMP])

	print('--------')

	new_data = Telemetry.objects.create(  # -------------- * * * -------------- SAVE TO DATABASE
	timestamp = data[TIMESTAMP], 
	accel_x   = data[ACCELX], 
	accel_y   = data[ACCELY], 
	accel_z   = data[ACCELZ], 
	gyro_x    = data[GYROX], 
	gyro_y    = data[GYROY], 
	gyro_z    = data[GYROZ],
	barometer = data[ALTITUDE],
	#temp = data[TEMP]
	)
	new_data.save()













