





	#had problems with only reading in a few data 
	print('-------------------------- * * * -------------------------- BEFORE')
	if (len(data) < 6):
		print("not enough data")
		continue
	print('-------------------------- * * * -------------------------- AFTER')
	
		#convert from string type
	for i in range(len(data)-1):
		if "NAN" in data[i]:
			data[i] = 0.0
			continue
		data[i] = float(data[i])

	#for the first few iterations, just take the 
	#accelerometer data to calibrate the offsets
	if(count <= 6):    # -------------- * * * -------------- NO TO 6, COLLECT UNTIL A BUTTON PRESSED
		if(count==6):
			ACCX_CALIB = ACCX_CALIB/6
			ACCY_CALIB = ACCY_CALIB/6
			ACCZ_CALIB = ACCZ_CALIB/6
		else:
			ACCX_CALIB += float(data[ACCELX])
			ACCY_CALIB += float(data[ACCELY])
			ACCZ_CALIB += float(data[ACCELZ])
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
	myAcceleration = acceleration.findInertialFrameAccel(data[ACCELX], data[ACCELY], data[ACCELZ], data[GYROX], data[GYROY], data[GYROZ], dt, [ACCX_CALIB, ACCY_CALIB, ACCZ_CALIB])
	#acceleration = (data[ACCELX],data[ACCELY],data[ACCELZ])
	#integrate to find velocity
	velocity = velocity+myAcceleration*dt

	#integrate to find position
	position = position + velocity*dt

	#append inertial frame acceleration velocity 
	#and position data to transmitted data
	data.append(myAcceleration.item(0))
	data.append(myAcceleration.item(1))
	data.append(myAcceleration.item(0)) 
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



	