from django.db import models

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

I_ACCEL_X = 0
I_ACCEL_Y = 0
I_ACCEL_Z = 0
VEL_X = 0
VEL_Y = 0
VEL_Z = 0
POS_X = 0
POS_Y = 0
POS_Z = 0
ABSTIME = 0

# Create your models here.
class Telemetry(models.Model):
	timestamp = models.FloatField(default = 0)
	#timestamp = models.CharField(max_length=200) # unsigned long
	#timestamp = models.DateTimeField()
	accel_x = models.FloatField(default = 0)
	accel_y = models.FloatField(default = 0)
	accel_z = models.FloatField(default = 0)
	gyro_x = models.FloatField(default = 0)
	gyro_y = models.FloatField(default = 0)
	gyro_z = models.FloatField(default = 0)
	barometer = models.FloatField(default = 0)
	temp = models.FloatField(default = 0)

	'''
	mag_x = models.FloatField(default=0)
	mag_y = models.FloatField(default=0)
	mag_z = models.FloatField(default=0)
	maghead = models.FloatField(default=0)
	altitude = models.FloatField(default=0)
	i_accel_x = models.FloatField(default=0)
	i_accel_y = models.FloatField(default=0)
	i_accel_z = models.FloatField(default=0)
	vel_x = models.FloatField(default=0)
	vel_y = models.FloatField(default=0)
	vel_z = models.FloatField(default=0)
	pos_x = models.FloatField(default=0)
	pos_y = models.FloatField(default=0)
	pos_z = models.FloatField(default=0)
	abstime = models.IntegerField(default=0)
	'''


	'''
	longitude = models.CharField(max_length=200, default="")
	latitude = models.CharField(max_length=200, default="")
	gpsAlt = models.CharField(max_length=200, default="")
	speed = models.CharField(max_length=200, default="")
	course = models.CharField(max_length=200, default="")
	'''

	def __str__(self):
		return str(self.timestamp) 

class IsLive(models.Model):
	isLive = models.BooleanField(default=False) 

	def __str__(self):
		return str(self.isLive)


class TimeInit(models.Model):
	timeInit = models.FloatField(default = 0)

	def __str__(self):
		return str(self.timeInit)

	def currTime(self):
		return self.timeInit




















