import numpy as np
import math

ACC_X_CALIB = 0.0
ACC_Y_CALIB = 0.0
ACC_Z_CALIB = 0.0
GYRO_X_CALIB = 0.0
GYRO_Y_CALIB = 0.0
GYRO_Z_CALIB = 0.0
NUM = 0.0

with open("test1.txt") as test:
	for line in test:
		data = line.split(",")
		ACC_X_CALIB = ACC_X_CALIB + float(data[0])
		ACC_Y_CALIB = ACC_Y_CALIB + float(data[2])
		ACC_Z_CALIB = ACC_Z_CALIB + float(data[1])
		GYRO_X_CALIB = GYRO_X_CALIB + float(data[3])
		GYRO_Y_CALIB = GYRO_Y_CALIB + float(data[5])
		GYRO_Z_CALIB = GYRO_Z_CALIB + float(data[4])
		NUM = NUM + 1.0
  
ACCEL_CALIB = [ ACC_X_CALIB / NUM , ACC_Y_CALIB / NUM , ACC_Z_CALIB / NUM ]
GYRO_CALIB = [ GYRO_X_CALIB / NUM , GYRO_Y_CALIB / NUM , GYRO_Z_CALIB / NUM ]

print("accel:")
print(str(ACCEL_CALIB))
print("gyro:")
print(str(GYRO_CALIB))