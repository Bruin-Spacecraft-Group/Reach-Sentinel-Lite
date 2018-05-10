import time
import datetime
import serial
import socket
import math
import numpy as np
import os
import django

from gps.GPS import GPSInit, saveCoor, processCoordinates, calcVelGPS
#from communication.sendUDP import initSocket, sendPacket, killSocket
from altimeter.altitudeCalculation import altitudeCalc
import acceleration
from serialStuff import openSerialPort, readFromSerial 
from DataObject import DataObject
#from accel import findInertialFrameAccel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reachSentinelLite.settings')
django.setup()

from graphs.models import Telemetry, IsLive  # exec(open("main.py").read())

print(
	'    +----------------------------------------------------------+\n'\
	'   /                   /                    /                / |\n'\
	'  /                   /                    /                /  |\n'\
	' +---------------------------------------------------------+   |\n'\
	' |  ______                    _____                        |   |\n'\
	' |  | ___ \           ()     /  ___|                       |   |\n'\
	' |  | |_/ /_ __ _   _ _ _ __ \ `--. _ __   __  _  ___ ___  |   |\n'\
	" |  | ___ \ '__| | | | | '_ \ `--. \ '_ \ / _\| |/ __/ _ \ |   |\n"\
	' |  | |_/ / |  | |_| | | | | /\__/ / |_) | (_ | | (__| __/ |   +\n'\
	' |  \____/|_|   \__,_|_|_| |_\____/| .__/ \__/|_|\___\___| |  /\n'\
	' |                                 | |                     | /\n'\
	' |                                 |_|                     |/\n'\
	' +------------------------- * * * -------------------------+\n')

# Database checks
if IsLive.objects.count() != 0:  # ------------------ * * * ------------------ REQUIRES TESTING
	for elem in IsLive.objects.all():
		elem.delete()

downlink = IsLive.objects.create() # ----------------- * * * ----------------- INITIALLY FALSE, ON BUTTON-CLICK IN DASH, TRUE

#Open serial port to recieve downlinked data
ser = openSerialPort('COM4')

#set positions of data in incoming csv packet
TIMESTAMP = 0
ACCELX = 1
ACCELY = 2
ACCELZ = 3
GYROX = 4
GYROY = 5
GYROZ = 6
GPSLAT = 7
GPSLON = 8
GPSALT = 9
GPSHOUR = 10
GPSMIN = 11
GPSSEC = 12
#MAGX = 7
#MAGY = 8
#MAGZ = 9
#MAGHEAD = 10
TEMP = 13
PRESS = 14
ALTITUDE = 15
BAROTEMP = 16

##Initiate variables
FIRST = True
oldtime = 0
oldGPSTime = 0
GPSInit()
myData = DataObject()
dropped = 0

count = 0
dataString = ''

##create plain text file to save raw data as backup for database
date = str(datetime.datetime.now())
FILENAME = 'Raw_Data/' + date
FILENAME = FILENAME.replace(':', '_')
txtfile = open(FILENAME, "w")
txtfile.write('Project Reach Raw Data starting at ' + date)

print('Telemetry initiated')

#Calibrate inertial gravity vector
myData.calibrate(ser, txtfile, [ACCELX, ACCELY, ACCELZ])

##Main Processing Loop
while True:
	data = readFromSerial(ser, txtfile)
	if data == -1: continue

	try:
		#Populate data object
		print('Populating data object...')
		myData.timestamp = data[TIMESTAMP]
		myData.accel_x = data[ACCELX]
		myData.accel_y = data[ACCELY]
		myData.accel_z = data[ACCELZ]
		print('step 1')
		myData.gyro_x = data[GYROX]
		myData.gyro_y = data[GYROY]
		myData.gyro_z = data[GYROZ]
		print('step 2')
		myData.gps_lat = data[GPSLON]
		myData.gps_lon = data[GPSLAT]
		myData.gps_alt = data[GPSALT]
		myData.gps_hour = data[GPSHOUR]
		myData.gps_min = data[GPSMIN]
		myData.gps_sec = data[GPSSEC]
		print('step 3')
		#myData.mag_x = data[MAGX]
		#myData.mag_y = data[MAGY]
		#myData.mag_z = data[MAGZ]
		#myData.mag_head = data[MAGHEAD]
		myData.temp = data[TEMP]
		myData.press = data[PRESS]
		myData.altitude = data[ALTITUDE]
		myData.baro_temp = data[BAROTEMP]

		print('populated')
		'''
		#Save raw data to database
		#TODO: Why are we doing this??
		new_data = Telemetry.objects.create(  #-------------- * * * -------------- SAVE TO DATABASE
			#timestamp=myData.timestamp, 
			timestamp = datetime.datetime.now(),
			accel_x=data[ACCELX], 
			accel_y= data[ACCELY], 
			accel_z= data[ACCELZ], 
			gyro_x=data[GYROX], 
			gyro_y=data[GYROY], 
			gyro_z= data[GYROZ],
			#mag_x = data[MAGX],
			#mag_y = data[MAGY],
			#mag_z = data[MAGZ],
			#maghead = data[MAGHEAD],
			barometer=data[ALTITUDE],
			temp=data[TEMP])
		new_data.save()
		'''
		###PROCESS
		#establish time elapsed
		dt = (myData.timestamp - oldtime)/1000.0 #convert ms to s
		print(myData.timestamp)
		print(oldtime)
		oldtime = myData.timestamp
		print(str(dt))
		'''
		append altitude calculated from pressure
		data.append(altitudeCalc(data[1]))
		'''
		#process acceleration
		acceleration.findInertialFrameAccel(myData, dt)
		print('found acceleration')
		#integrate to find velocity and positino
		acceleration.calculateVelocityAndPosition(myData, dt)
		print('found vel and pos')
		#Process GPS coordinates
		if myData.gps_sec != oldGPSTime:
			oldGPSTime = myData.gps_sec
			processCoordinates(myData.gps_lon, myData.gps_lat, myData.gps_alt)
			print('processed coordinates')
		'''
		#append absolute time
		data.append(time.time())
		'''
		myData.printData()
		#print(dropped)

		######SAVE TO DATABASE

	except:
		print('failed\n')
		#print(dropped)
		continue #maybe this should be a continue?
		

	#TODO -- might actually want to implement the data object. 
	#At this point it's confusing where the processed data ends up
	'''
	try:
		new_data = Telemetry.objects.create(  #-------------- * * * -------------- SAVE TO DATABASE
			timestamp=myData.timestamp, 
			accel_x=data[6], 
			accel_y= data[7], 
			accel_z= data[8], 
			gyro_x=data[3], 
			gyro_y=data[4], 
			gyro_z= data[5],
			barometer=data[1],
			temp=data[2])
		new_data.save()
	'''
