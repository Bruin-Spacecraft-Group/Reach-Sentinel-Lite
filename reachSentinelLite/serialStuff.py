import serial

def openSerialPort(myPort):
	try:
		print("Opening Serial Port...")
		#initiate serial port to read data from
		ser = serial.Serial(
		    port=myPort,
		    baudrate=9600,
		    timeout=5, #give up reading after 5 seconds
		    parity=serial.PARITY_ODD,
		    stopbits=serial.STOPBITS_TWO,
		    bytesize=serial.SEVENBITS
		)
		print("connected to port " + myPort)
		return ser
	except:
		print("<== Error connecting to " + myPort + " ==>")
		exit()

def readFromSerial(ser, txtfile):
	if ser.isOpen():
		dataString = ''
		try:
			#get data
			print('reading...')
			dataString = str(ser.readline())
			print("Recieved: " + dataString)
			'''
			if(dataString == "b''"):
				dropped += 1
			'''
		except:
			print("could not read")
			return -1
		
		#write to text file
		try:
			print('writing to text file')
			txtfile.write(dataString)
			txtfile.flush()
		except:
			print('Could not write to text file')
			pass

		#create data array
		try:
			#cut off extra characters
			#first two characters are b'
			#last 5, are \r\n'
			dataString = dataString[2:len(dataString)-5]
			data = dataString.split(",")
			
			#ensure full packet recieved
			if (len(data) < 6):
				print("Not enough data")
				return -1
			
			#adjust for NANs
			print('Checking for NANs')
			nans = 0
			for i in range(len(data)-1):
				if "NAN" in data[i]:
					data[i] = float('nan')
					nans += 1
					continue
				data[i] = float(data[i])
			print('NANs: ' + str(nans))
			return data
		except:
			print("Error creating data array")
			return -1
	else:
		print("ser not open")
		return -1