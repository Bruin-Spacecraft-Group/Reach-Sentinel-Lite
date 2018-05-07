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
try:
	print("Opening Serial Port...")
	#initiate serial port to read data from
	SERIAL_PORT = 'COM4'
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=9600,
	    timeout=5, #give up reading after 5 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print("connected to port " + SERIAL_PORT)
except:
	print("<== Error connecting to " + SERIAL_PORT + " ==>")
	#exit()

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

##Main Processing Loop
while ser.isOpen():
	
	'''if ser.isOpen():
					print('ser is open')
					pass
				else:
					print("serial is not open")
					continue'''

	try:
		#get data
		print('reading...')
		dataString = str(ser.readline())
		print(dataString)
		'''
		if(dataString == "b''"):
			dropped += 1
		'''
	except:
		print("could not read")
		continue

	try:
		print('writing to text file')
		txtfile.write(dataString)
		txtfile.flush()
	except:
		pass

	try:
		#cut off extra characters
		#first two characters are b'
		#last 5, are \r\n'
		dataString = dataString[2:len(dataString)-5]
		print('Received: ' + dataString)
		data = dataString.split(",")
		#had problems with only reading in a few data 
		if (len(data) < 6):
			print("not enough data")
			continue
		
		#adjust for NANs
		print('checking for NANs')
		nans = 0
		for i in range(len(data)-1):
			if "NAN" in data[i]:
				data[i] = float('nan')
				nans += 1
				continue
			data[i] = float(data[i])
		print('NANs: ' + str(nans))

		#Populate data object
		print('Populating data object...')
		myData.timestamp = data[TIMESTAMP]
		myData.accel_x = data[ACCELX]
		myData.accel_y = data[ACCELY]
		myData.accel_z = data[ACCELZ]
		myData.gyro_x = data[GYROX]
		myData.gyro_y = data[GYROY]
		myData.gyro_z = data[GYROZ]
		myData.gps_lat = data[GPSLON]
		myData.gps_lon = data[GPSLAT]
		myData.gps_alt = data[GPSALT]
		myData.gps_hour = data[GPSHOUR]
		myData.gps_min = data[GPSMIN]
		myData.gps_sec = data[GPSSEC]
		#myData.mag_x = data[MAGX]
		#myData.mag_y = data[MAGY]
		#myData.mag_z = data[MAGZ]
		#myData.mag_head = data[MAGHEAD]
		myData.temp = data[TEMP]
		myData.press = data[PRESS]
		myData.altitude = data[ALTITUDE]
		myData.baro_temp = data[BAROTEMP]

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

		#for the first few iterations, just take the 
		#accelerometer data to calibrate the offsets

		if(count<6):
			print('Calibrating...')
			myData.accx_calib += myData.accel_x
			myData.accy_calib += myData.accel_y
			myData.accz_calib += myData.accel_z
			count+=1
			#establish spacecraft time
			oldtime = myData.timestamp
		
		else:
			print('processing...')
			if(count==6):
				myData.accx_calib = myData.accx_calib/6
				myData.accy_calib = myData.accy_calib/6
				myData.accz_calib = myData.accz_calib/6
				count+=1
				myData.printCalibration()
				#print('Calibration: ' + str(ACCX_CALIB) + ', ' + str(ACCY_CALIB) + ', ' + str(ACCZ_CALIB))
		
			##DO STUFF WITH DATA
			#establish time elapsed
			dt = (myData.timestamp - oldtime)/1000.0 #convert ms to s
			oldtime = myData.timestamp
			print(str(dt))
			'''
			append altitude calculated from pressure
			data.append(altitudeCalc(data[1]))
			'''
			#process acceleration
			acceleration.findInertialFrameAccel(myData, dt)
			#myAcceleration = acceleration.findInertialFrameAccel(data[ACCELX], data[ACCELY], data[ACCELZ], data[GYROX], data[GYROY], data[GYROZ], dt, [ACCX_CALIB, ACCY_CALIB, ACCZ_CALIB])
			print('found acceleration')
			#integrate to find velocity and positino
			acceleration.calculateVelocityAndPosition(myData, dt)
			print('found vel and pos')
			#Process GPS coordinates
			if myData.gps_sec != oldGPSTime:
				processCoordinates(myData.gps_lon, myData.gps_lat, myData.gps_alt)
				print('processed coordinates')
			'''
			#append absolute time
			data.append(time.time())
			'''
			finalData = ""
			for i in range(len(data)-1):
				#print data[i]
				finalData = finalData + str(data[i]) + ", "
				'''
				finalData contents should be as follows, 
				as a string separated by commas:
				relative spacecraft time 
				raw accelX
				raw accelY
				raw accelZ
				gyroX
				gyroY
				gyroZ
				magX - NO
				magY - NO
				magZ - NO
				magHead - NO
				temp(C)
				altitude
				inertial accelX
				inertial accelY
				inertial accelZ
				velX
				velY
				velZ
				posX
				posY
				posZ
				absTime - NO
				'''
			print(finalData)
			myData.printData()
			print(dropped)
	except:
		print('failed\n')
		print(dropped)
		continue #maybe this should be a continue?
		######SAVE TO DATABASE

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
