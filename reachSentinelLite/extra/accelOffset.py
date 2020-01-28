import numpy as np
import math

ACCX_CALIB = 0.0
ACCY_CALIB = 0.0
ACCZ_CALIB = 0.0
NUM = 0.0

with open("test1.txt") as test:
	for line in test:
		accel = line.split(",")
		ACCX_CALIB = ACCX_CALIB + float(accel[0])
		ACCY_CALIB = ACCY_CALIB + float(accel[1])
		ACCZ_CALIB = ACCZ_CALIB + float(accel[2])
		NUM = NUM + 1.0
  
CALIB = [ ACCX_CALIB / NUM , ACCY_CALIB / NUM , ACCZ_CALIB / NUM ]
print(str(CALIB))