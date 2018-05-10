import math
from serialStuff import readFromSerial
class DataObject:
	"""data structure for telemetry data"""
	def __init__(self):
		self.timestamp = float('nan')
		self.accel_x = float('nan')
		self.accel_y = float('nan')
		self.accel_z = float('nan')
		self.gyro_x = float('nan')
		self.gyro_y = float('nan')
		self.gyro_z = float('nan')
		self.gps_lat = float('nan')
		self.gps_lon = float('nan')
		self.gps_alt = float('nan')
		self.gps_hour = float('nan')
		self.gps_min = float('nan')
		self.gps_sec = float('nan')
		#self.mag_x = float('nan')
		#self.mag_y = float('nan')
		#self.mag_z = float('nan')
		#self.mag_head = float('nan')
		self.temp = float('nan')
		self.press = float('nan')
		self.altitude = float('nan')
		self.baro_temp = float('nan')

		self.vel_x, self.vel_y, self.vel_z = 0, 0, 0
		self.pos_x, self.pos_y, self.pos_z = 0, 0, 0

		self.accx_calib, self.accy_calib, self.accz_calib = 0, 0, 0

	def calibrate(self, ser, txtfile, accelIndex):
		iterations = float(input("How many iterations for calibration? "))
		i = 0
		x_calib, y_calib, z_calib = 0,0,0
		print(accelIndex)
		while i < iterations:
			data = readFromSerial(ser, txtfile)
			if data == -1:
				continue
			x_calib += data[accelIndex[0]]
			y_calib += data[accelIndex[1]]
			z_calib += data[accelIndex[2]]	
			i += 1

		if iterations != 0:			
			self.accx_calib = x_calib/iterations
			self.accy_calib = y_calib/iterations
			self.accz_calib = z_calib/iterations

		self.printCalibration()

	def printCalibration(self):
		print('Calibration: ' + str(self.accx_calib) + ','+ str(self.accy_calib) + ','+ str(self.accz_calib))

	def printSpacecraftTime(self):
		hours = math.floor(self.timestamp/(60*60*1000.0))
		minutes = math.floor((self.timestamp - hours*60*60*1000)/(60*1000))
		seconds = (self.timestamp - hours*60*60*1000 - minutes*60*1000)/1000.0
		print('Spacecraft time ' + str(hours) + ':' + str(minutes) + ':' + str(seconds))

	def printData(self):
		print('Final Data:\n')
		self.printSpacecraftTime()
