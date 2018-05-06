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

# Dabatase checks
if IsLive.objects.count() != 0:  # ------------------ * * * ------------------ REQUIRES TESTING
	for elem in IsLive.objects.all():
		elem.delete()

downlink = IsLive.objects.create() # ----------------- * * * ----------------- INITIALLY FALSE, ON BUTTON-CLICK IN DASH, TRUE

try:
	print("Opening Serial Port...")
	#initiate serial port to read data from
	SERIAL_PORT = 'COM4'
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=9600,
	    timeout=3, #give up reading after 3 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print("connected to port " + SERIAL_PORT)
except:
	print("<== Error connecting to " + SERIAL_PORT + " ==>")
	exit()

##Initiate variables
FIRST = True

lat2 = 0
lon2 = 0
GPSInit()
velocity = np.matrix([0,0,0]).T
position = np.matrix([0,0,0]).T

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
PRES = 14
ALTITUDE = 15
BAROTEMP = 16

tots_not_launch = 1
count = 0
dataString = ''

##create plain text file to save raw data as backup for database
date = str(datetime.datetime.now())
FILENAME = 'Raw_Data/' + date
FILENAME = FILENAME.replace(':', '_')
txtfile = open(FILENAME, "w")
txtfile.write('Project Reach Raw Data starting at ' + date)

##Main Processing Loop
while ser.isOpen():
	try:
		#get data
		dataString = ser.readline()
	except:
		continue

	try:
		txtfile.write(dataString)
		txtfile.flush()
	except:
		pass

	try:
		#cut off extra characters
		#first two characters are b'
		#last 5, I don't actually know....
		dataString = dataString[2:len(dataString)-5]
		print('Received: ' + dataString)
		data = dataString.split(",")

		#TODO: check whether this is right/necessary
		#can have multiple data types in python - no need to change NAN into a float
		#adjust for NANs
		for i in range(len(data)-1):
			if "NAN" in data[i]:
				#data[i] = 0.0
				continue
			data[i] = float(data[i])

		#Save raw data to database
		#TODO: Why are we doing this??
		new_data = Telemetry.objects.create(  #-------------- * * * -------------- SAVE TO DATABASE
			#timestamp=data[TIMESTAMP], 
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

		#for the first few iterations, just take the 
		#accelerometer data to calibrate the offsets

		if(count<6):
			print('Calibrating...')
			ACCX_CALIB += data[ACCELX]
			ACCY_CALIB += data[ACCELY]
			ACCZ_CALIB += data[ACCELZ]
			count+=1
			#establish spacecraft time
			oldtime = float(data[TIMESTAMP])
		
		else:
			if(count==6):
				ACCX_CALIB = ACCX_CALIB/6
				ACCY_CALIB = ACCY_CALIB/6
				ACCZ_CALIB = ACCZ_CALIB/6
				count+=1
				print('Calibration: ' + str(ACCX_CALIB) + ', ' + str(ACCY_CALIB) + ', ' + str(ACCZ_CALIB))
		
			#had problems with only reading in a few data 
			if (len(data) < 6):
				print("not enough data")
				continue
		
			#DO STUFF WITH DATA
			'''
			if (len(data) < 12):
				gpsRecieved = False
				print "no coordinates"
			else: 
				gpsRecieved = True
			'''
			#establish time elapsed
			dt = (data[TIMESTAMP] - oldtime)/1000.0 #convert ms to s
			oldtime = data[TIMESTAMP]
			'''
			append altitude calculated from pressure
			data.append(altitudeCalc(data[1]))
			'''
			#process acceleration
			myAcceleration = acceleration.findInertialFrameAccel(data[ACCELX], data[ACCELY], data[ACCELZ], data[GYROX], data[GYROY], data[GYROZ], dt, [ACCX_CALIB, ACCY_CALIB, ACCZ_CALIB])
			
			#integrate to find velocity
			velocity = velocity + myAcceleration*dt

			#integrate to find position
			position = position + velocity*dt

			#append inertial frame acceleration velocity 
			#and position data to transmitted data
			data.append(myAcceleration.item(0))
			data.append(myAcceleration.item(1))
			data.append(myAcceleration.item(0)) 
			data.append(velocity.item(0)) 
			data.append(velocity.item(1))
			data.append(velocity.item(2))
			data.append(position.item(0))
			data.append(position.item(1))
			data.append(position.item(2))
		
			
			#Process GPS coordinates
			if data[GPSSEC] != oldGPSTime:
				longitude = data[GPSLON]
				latitude = data[GPSLAT]
				latDeg = math.floor(latitude)
				lonDeg = math.floor(longitude)
		
				latMin = float(latitude) - latDeg
				lonMin = float(longitude) - lonDeg
			    
				lat = float(latDeg)+float(latMin)/60
				lon = float(lonDeg)-float(lonMin)/60
			    
				saveCoor(lon, lat, data[GPSALT])
			    
			    #speed calculation from gps data:
				#push the last new value to the old and then set the new value 
				lat1 = lat2
				lat2 = lat
				lon1 = lon2
				lon2 = lon

				dt = data[GPSSEC] - oldGPSTime
				if dt < 0:
					dt = data[GPSSEC] + 60 - oldGPSTime
				#specific to GPS because GPS not expected as often
				oldGPSTime = data[GPSSEC]
				#calcVelGPS(lat1, lon1, lat2, lon2, dt)
		
				print("sending:")
			
			
			#append absolute time
			data.append(time.time())
			
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
				magX
				magY
				magZ
				magHead
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
				absTime
				'''
			print(finalData)
	except:
		pass
		######SAVE TO DATABASE

	'''
	new_data = Telemetry.objects.create(  -------------- * * * -------------- SAVE TO DATABASE
	timestamp=data[0], 
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