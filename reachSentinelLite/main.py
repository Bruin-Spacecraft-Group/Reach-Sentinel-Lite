import time
import datetime
import serial
import socket
import math
import numpy as np

from gps.GPS import GPSInit, saveCoor, processCoordinates, calcVelGPS
from communication.sendUDP import initSocket, sendPacket, killSocket
from altimeter.altitudeCalculation import altitudeCalc
import accel
#from accel import findInertialFrameAccel

from graphs.models import Telemetry, IsLive  # exec(open("main.py").read())

print(
	'______            _       _____                      \n'\
	'| ___ \          (_)     /  ___|                     \n'\
	'| |_/ /_ __ _   _ _ _ __ \ `--. _ __   __ _  ___ ___ \n'\
	"| ___ \ '__| | | | | '_ \ `--. \ '_ \ / _` |/ __/ _ \ \n"\
	'| |_/ / |  | |_| | | | | /\__/ / |_) | (_| | (_|  __/\n'\
	'\____/|_|   \__,_|_|_| |_\____/| .__/ \__,_|\___\___|\n'\
	'                               | |                   \n'\
	'                               |_|        \n')


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
MAGX = 7
MAGY = 8
MAGZ = 9
MAGHEAD = 10
TEMP = 11
ALTITUDE = 12

tots_not_launch = 1
count = 0

#create plain text file to save raw data as backup for database
date = str(datetime.datetime.now())
FILENAME = 'Raw_Data/' + date
FILENAME = FILENAME.replace(':', '_')
txtfile = open(FILENAME, "w")
txtfile.write('Project Reach Raw Data starting at ' + date)

##Main Processing Loop
while ser.isOpen():
	#get data
	dataString = ser.readline()
	txtfile.write(dataString)
	print('"' + dataString)
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
	'''
	new_data = Telemetry.objects.create(  -------------- * * * -------------- SAVE TO DATABASE
	timestamp=data[TIMESTAMP], 
	accel_x=data[ACCELX], 
	accel_y= data[ACCELY], 
	accel_z= data[ACCELZ], 
	gyro_x=data[GYROX], 
	gyro_y=data[GYROY], 
	gyro_z= data[GYROZ],
	mag_x = data[MAGX],
	mag_y = data[MAGY],
	mag_z = data[MAGZ],
	maghead = data[MAGHEAD],
	barometer=data[ALTITUDE],
	temp=data[TEMP])
	new_data.save()
	'''

	#had problems with only reading in a few data 
	if (len(data) < 6):
		print("not enough data")
		continue
	#for the first few iterations, just take the 
	#accelerometer data to calibrate the offsets
	if(count <= 6):
		if(count==6):
			ACCX_CALIB = ACCX_CALIB/6
			ACCY_CALIB = ACCY_CALIB/6
			ACCZ_CALIB = ACCZ_CALIB/6
		else:
			ACCX_CALIB += data[ACCELX]
			ACCY_CALIB += data[ACCELY]
			ACCZ_CALIB += data[ACCELZ]
		count += 1
		continue
		
	#establish spacecraft time
	if(FIRST == True):
		FIRST = False
		oldtime = float(data[TIMESTAMP])
		#since dt cannot be established, skip
		#TODO save first data packet's raw data
		continue

	#DO STUFF WITH DATA
	#convert from string type
	for i in range(len(data)-1):
		data[i] = float(data[i])
	'''
	if (len(data) < 12):
		gpsRecieved = False
		print "no coordinates"
	else: 
		gpsRecieved = True
	'''
	#establish time elapsed
	dt = (data[TIMESTAMP] - oldtime)/1000 #convert ms to s
	oldtime = data[TIMESTAMP]

	#append altitude calculated from pressure
	#data.append(altitudeCalc(data[1]))

	#process acceleration
	acceleration = accel.findInertialFrameAccel(data[ACCELX], data[ACCELY], data[ACCELZ], data[GYROX], data[GYROY], data[GYROZ], dt, [ACCX_CALIB, ACCY_CALIB, ACCZ_CALIB])
	
	#integrate to find velocity
	velocity = velocity+acceleration*dt

	#integrate to find position
	position = position + velocity*dt

	#append inertial frame acceleration velocity 
	#and position data to transmitted data
	data.append(acceleration.item(0))
	data.append(acceleration.item(1))
	data.append(acceleration.item(2))
	data.append(velocity.item(0)) 
	data.append(velocity.item(1))
	data.append(velocity.item(2))
	data.append(position.item(0))
	data.append(position.item(1))
	data.append(position.item(2))

	'''
	#Process GPS coordinates
	if data[9] != oldGPSTime:
		longitude = data[10]
		latitude = data[11]
		latDeg = math.floor(latitude)
		lonDeg = math.floor(longitude)

		latMin = float(latitude) - latDeg
		lonMin = float(longitude) - lonDeg
	    
		lat = float(latDeg)+float(latMin)/60
	 	lon = float(lonDeg)-float(lonMin)/60
	    
		saveCoor(lon, lat, data[12])
	    
	    #speed calculation from gps data:
		#push the last new value to the old and then set the new value 
		lat1 = lat2
	 	lat2 = lat
		lon1 = lon2
		lon2 = lon

		dt = data[9] - oldGPSTime
		#specific to GPS because GPS not expected as often
		oldGPSTime = data[9]
		#calcVelGPS(lat1, lon1, lat2, lon2, dt)

		print "sending:"
	'''
	
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
	#sock.sendto(finalData, (SEND_TO_IP, SEND_TO_PORT))
#killSocket(sock)
