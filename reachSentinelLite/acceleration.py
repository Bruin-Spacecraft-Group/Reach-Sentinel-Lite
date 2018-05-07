import numpy as np
import math

#ACCX_CALIB = -20
#ACCY_CALIB = -10
#ACCZ_CALIB = 13


cum_rot = np.matrix([[1,0,0],[0,1,0],[0,0,1]])


#GYRX_CALIB = -80.83
#GYRY_CALIB = 64.81
#GYRZ_CALIB = -52.35

#rot
def rotationMatrixToEulerAngles(R) :
 
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])

def gyrotoeuler(gyro,pos,dt):
    sinPhi = math.sin(pos[0])
    cosPhi = math.cos(pos[0])
    cosTheta = math.cos(pos[1])
    tanTheta = math.tan(pos[1])
    
    d= np.matrix([
           [1,math.sin(pos[0])*math.tan(pos[1]),math.cos(pos[0])*math.tan(pos[1])],
           [0,math.cos(pos[0]),-math.sin(pos[0])],
           [0,math.sin(pos[0])/math.cos(pos[1]),math.cos(pos[0])/math.cos(pos[1])]
    ])
    cat = d*np.matrix(gyro).T
    return np.matrix(pos)+np.matrix(cat)*dt

'''
def findInertialFrameAccel(accX, accY, accZ, gyrX, gyrY, gyrZ, dt,inital_g):
    global cum_rot
    g_norm = [[accX],[accY],[accZ]]
    for i in range(0,3):
        g_norm[i]= g_norm[i][0]
    g_norm = np.matrix(g_norm)
    holder = [gyrX,gyrY,gyrZ]
    for i in range(0,3):
       if abs(holder[i]) <0.05:
            holder[i]=0
    holder = gyrotoeuler(holder,rotationMatrixToEulerAngles(cum_rot),dt).T
    z_rot = np.matrix([
        [ math.cos(math.radians(holder.item(2))) , -math.sin(math.radians(holder.item(2))) ,  0 ],
        [ math.sin(math.radians(holder.item(2))) , math.cos(math.radians(holder.item(2)))  , 0 ],
        [ 0 , 0 , 1 ]
    ])
    y_rot = np.matrix([
        [ math.cos(math.radians(holder.item(1)))  , 0 , math.sin(math.radians(holder.item(1))) ],
        [ 0 , 1 , 0 ],
        [ -math.sin(math.radians(holder.item(1))) ,  0 , math.cos(math.radians(holder.item(1))) ]
    ])
    x_rot = np.matrix([
        [ 1 , 0 , 0 ],
        [ 0 , math.cos(math.radians(holder.item(0))) , -math.sin(math.radians(holder.item(0))) ],
        [ 0 , math.sin(math.radians(holder.item(0))) , math.cos(math.radians(holder.item(0))) ]    	    
    ])
    total_rot = z_rot*y_rot*x_rot
    cum_rot = cum_rot *total_rot
    inertal_acc = cum_rot*g_norm.T
    inertal_acc = inertal_acc - np.matrix(inital_g).T
    return inertal_acc
'''
def findInertialFrameAccel(dataObject, dt):
    global cum_rot
    print(dataObject.accel_x)
    g_norm = [dataObject.accel_x,dataObject.accel_y,dataObject.accel_z]
    '''for i in range(0,3):
                    g_norm[i]= g_norm[0][i]'''
    g_norm = np.matrix(g_norm)
    holder = [dataObject.gyro_x,dataObject.gyro_y,dataObject.gyro_z]
    for i in range(0,3):
       if abs(holder[i]) <0.05:
            holder[i]=0
    holder = gyrotoeuler(holder,rotationMatrixToEulerAngles(cum_rot),dt).T
    z_rot = np.matrix([
        [ math.cos(math.radians(holder.item(2))) , -math.sin(math.radians(holder.item(2))) ,  0 ],
        [ math.sin(math.radians(holder.item(2))) , math.cos(math.radians(holder.item(2)))  , 0 ],
        [ 0 , 0 , 1 ]
    ])
    y_rot = np.matrix([
        [ math.cos(math.radians(holder.item(1)))  , 0 , math.sin(math.radians(holder.item(1))) ],
        [ 0 , 1 , 0 ],
        [ -math.sin(math.radians(holder.item(1))) ,  0 , math.cos(math.radians(holder.item(1))) ]
    ])
    x_rot = np.matrix([
        [ 1 , 0 , 0 ],
        [ 0 , math.cos(math.radians(holder.item(0))) , -math.sin(math.radians(holder.item(0))) ],
        [ 0 , math.sin(math.radians(holder.item(0))) , math.cos(math.radians(holder.item(0))) ]         
    ])

    total_rot = z_rot*y_rot*x_rot
    cum_rot = cum_rot *total_rot
    inertal_acc = cum_rot*g_norm.T
    inertal_acc = inertal_acc - np.matrix([dataObject.accx_calib,dataObject.accy_calib,dataObject.accz_calib,]).T
    
    dataObject.accel_x = inertal_acc.item(0)
    dataObject.accel_x = inertal_acc.item(1)
    dataObject.accel_x = inertal_acc.item(2)

def calculateVelocityAndPosition(dataObject, dt):
    acceleration = np.matrix([dataObject.accel_x, dataObject.accel_y, dataObject.accel_z]).T
    velocity = np.matrix([dataObject.vel_x, dataObject.vel_y, dataObject.vel_z]).T
    position = np.matrix([dataObject.pos_x, dataObject.pos_y, dataObject.pos_z]).T

    velocity = velocity + acceleration*dt
    position = position + velocity*dt

    dataObject.vel_x = velocity.item(0)
    dataObject.vel_y = velocity.item(1)
    dataObject.vel_z = velocity.item(2)

    dataObject.pos_x = position.item(0)
    dataObject.pos_y = position.item(1)
    dataObject.pos_z = position.item(2)