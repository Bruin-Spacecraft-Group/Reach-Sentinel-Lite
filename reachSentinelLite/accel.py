import numpy as np
import math

ACCX_CALIB = -20
ACCY_CALIB = -10
ACCZ_CALIB = 13

GYRX_CALIB = -80.83
GYRY_CALIB = 64.81
GYRZ_CALIB = -52.35

#rot
def createRotation(x, y, z):
	rotation = [
		[math.cos( y * math.pi/180 ) * math.cos( z * math.pi/180 ) , math.cos( z * math.pi/180 ) * math.sin( x * math.pi/180 ) * math.sin( y * math.pi/180 ) - math.cos( x * math.pi/180 ) * math.sin( z * math.pi/180 ) , math.cos( x * math.pi/180 ) * math.cos( z * math.pi/180 ) * math.sin( y * math.pi/180 ) + math.sin( x * math.pi/180 ) * math.sin( z * math.pi/180 )],
		[math.cos( y * math.pi/180 ) * math.sin( z * math.pi/180 ) , math.cos( x * math.pi/180 ) * math.cos( z * math.pi/180 ) + math.sin( x * math.pi/180 ) * math.sin( y * math.pi/180 ) * math.sin( z * math.pi/180 ) , math.cos( x * math.pi/180 ) * math.sin( y * math.pi/180 ) * math.sin( z * math.pi/180 ) - math.cos( z * math.pi/180 ) * math.sin( x * math.pi/180 )],
		[-math.sin( y * math.pi/180 ) , math.cos( y * math.pi/180 ) * math.sin( x * math.pi/180 ) , math.cos( x * math.pi/180 ) * math.cos( y * math.pi/180 )]
		]
	return rotation

#multi
def multiplyMatrix(a,b):
	result = [[0,0,0],[0,0,0],[0,0,0]]
	for i in range(3): #aRow
		for j in range(3): #bColumn
			for k in range(3): #aColumn
				result[i][j] += a[i][k] * b[k][j]
	return result

#sum
def dotProduct(a,b):
	return np.dot(a,b)
#multiply
def rotate(accel, rotation):
	a = accel[0]*rotation[0][0] + accel[1]*rotation[1][0] + accel[2]*rotation[2][0]
	b = accel[0]*rotation[0][1] + accel[1]*rotation[1][1] + accel[2]*rotation[2][1]
	c = accel[0]*rotation[0][2] + accel[1]*rotation[1][2] + accel[2]*rotation[2][2]

	accel[0] = a
	accel[1] = b
	accel[2] = c
	return accel

def findInertialFrameAccel(accX, accY, accZ, gyrX, gyrY, gyrZ, dt, accX_offset, accY_offset, accZ_offset):
	acceleration = [ accX , accY , accZ ]
	net_rotation = createRotation(1,2,1)
	#velocity = [0,0,0]
	#position = [0,0,0]
	
	acceleration[0] = acceleration[0] * 9.8 / 256 - accX_offset
	acceleration[1] = acceleration[1] * 9.8 / 256 - accY_offset
	acceleration[2] = acceleration[2] * 9.8 / 256 - accZ_offset

	#note I skipped the gyro absolute value tests
	gyrX = gyrX + GYRX_CALIB
	gyrY = gyrY + GYRY_CALIB
	gyrZ = gyrZ + GYRZ_CALIB

	net_rotation = multiplyMatrix(net_rotation, createRotation(gyrX*dt/1000, gyrY*dt/1000, gyrZ*dt/1000))
	
	acceleration = rotate(acceleration, net_rotation)
	
	#subtract g from z?
	acceleration[2] = acceleration[2] - 9.8

	#note I left off the cut off tests for acceleration

	print("acceleration: " + str(acceleration))
	#print("velocity: " + str(velocity))
	#print("position: " + str(position))

	return acceleration
