import numpy as np
import math
import time

ACCX_CALIB = 2.186
ACCY_CALIB = 27.731
ACCZ_CALIB = -255.946

GYRX_CALIB = -62.749
GYRY_CALIB = -57.682
GYRZ_CALIB = 77.826
#store three data points
accelHistory = [[0,0,0],[0,0,0],[0,0,0]]

velocity = [0,0,0]
position = [0,0,0]

dt = 0.1

startTime = time.time()

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


net_rotation = createRotation(0,0,0)

def adamsBashforth(accelHistory, accX, accY, accZ, gyrX, gyrY, gyrZ, dt, net_rotation):
	acceleration = [accX + ACCX_CALIB, accY + ACCY_CALIB, accZ + ACCZ_CALIB]
	

	acceleration[0] = acceleration[0] * 9.8 / 256
	acceleration[1] = acceleration[1] * 9.8 / 256
	acceleration[2] = acceleration[2] * 9.8 / 256
	
	#note I skipped the gyro absolute value tests
	gyrX = gyrX + GYRX_CALIB
	gyrY = gyrY + GYRY_CALIB
	gyrZ = gyrZ + GYRZ_CALIB

	net_rotation = multiplyMatrix(net_rotation, createRotation(gyrX*dt/1000, gyrY*dt/1000, gyrZ*dt/1000))
	
	acceleration = rotate(acceleration, net_rotation)
	
	#subtract g from z?
	#acceleration[2] = acceleration[2] - 9.8
	
	#fourth order method
	velocity[0] = velocity[0] + dt/24*(55*acceleration[0] - 59*accelHistory[0][0] + 37*accelHistory[1][0] -9*accelHistory[2][0])
	velocity[1] = velocity[1] + dt/24*(55*acceleration[0] - 59*accelHistory[0][1] + 37*accelHistory[1][1] -9*accelHistory[2][1])
	velocity[2] = velocity[2] + dt/24*(55*acceleration[0] - 59*accelHistory[0][2] + 37*accelHistory[1][2] -9*accelHistory[2][2])

	accelHistory[2][0] = accelHistory[1][0]
	accelHistory[2][1] = accelHistory[1][1]
	accelHistory[2][2] = accelHistory[1][2]

	accelHistory[1][0] = accelHistory[0][0]
	accelHistory[1][1] = accelHistory[0][1]
	accelHistory[1][2] = accelHistory[0][2]
	
	accelHistory[0][0] = acceleration[0]
	accelHistory[0][1] = acceleration[1]
	accelHistory[0][2] = acceleration[2]
	
	'''
	#second order
	velocity[0] = velocity[0] + 3/2*dt*acceleration[0] - 1/2*dt*accelHistory[0][0]
	velocity[1] = velocity[1] + 3/2*dt*acceleration[1] - 1/2*dt*accelHistory[0][1]
	velocity[2] = velocity[2] + 3/2*dt*acceleration[2] - 1/2*dt*accelHistory[0][2]
	
	accelHistory[0][0] = acceleration[0]
	accelHistory[0][1] = acceleration[1]
	accelHistory[0][2] = acceleration[2]
	'''
	#calculate position simply
	position[0] = position[0] + velocity[0]*dt
	position[1] = position[1] + velocity[1]*dt
	position[2] = position[2] + velocity[2]*dt

	#print "rotation" + str(net_rotation[2])
	print("acceleration: " + str(acceleration))
	print("velocity: " + str(velocity))
	print("position: " + str(position))

'''
I don't think the Runge-Kutta Method is actually applicable 
since I don't have a function to model off of
#Runge-Kutta Method
def f(v, a):
    return(v + a*dt)

def rk4(f, velocity, acceleration):
    for i in range(3):
	    k1 = dt * f(velocity[i], acceleration[i])
	    k2 = dt * f(velocity[i] + 0.5 * dt, acceleration[i] + 0.5 * k1)
	    k3 = dt * f(velocity[i] + 0.5 * dt, acceleration[i] + 0.5 * k2)
	    k4 = dt * f(velocity[i] + dt, acceleration[i] + k3)
	    acceleration[i] = velocity[i] + (k1 + k2 + k2 + k3 + k3 + k4) / 6
    


    print "acceleration: " + str(acceleration)
	print "velocity: " + str(velocity)
	print "position: " + str(position)
'''


with open("test1.txt") as dataFile:
	for line in dataFile:
		data = line.split(',')
		adamsBashforth(accelHistory, float(data[0]),float(data[2]),float(data[1]),float(data[3]),float(data[4]),float(data[5]), dt, net_rotation)

endTime = time.time()
timeElapsed = endTime - startTime
print(str(timeElapsed))