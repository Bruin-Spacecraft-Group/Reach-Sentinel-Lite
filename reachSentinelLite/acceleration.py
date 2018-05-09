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
