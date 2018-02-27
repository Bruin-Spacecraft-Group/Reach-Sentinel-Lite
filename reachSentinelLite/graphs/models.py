from django.db import models

# Create your models here.
class Telemetry(models.Model):
	timestamp = models.CharField(max_length=200)
	#timestamp = models.DateTimeField()
	accel_x = models.IntegerField()
	accel_y = models.IntegerField()
	accel_z = models.IntegerField()
	gyro_x = models.FloatField()
	gyro_y = models.FloatField()
	gyro_z = models.FloatField()
	barometer = models.FloatField()
	temp = models.FloatField()
	'''
	gpsTime = models.CharField(max_length=200, default="")
	longitude = models.CharField(max_length=200, default="")
	latitude = models.CharField(max_length=200, default="")
	gpsAlt = models.CharField(max_length=200, default="")
	speed = models.CharField(max_length=200, default="")
	course = models.CharField(max_length=200, default="")
	'''

	def __str__(self):
		return self.timestamp 

class IsLive(models.Model):
	isLive = models.BooleanField(default=False) 

	def __str__(self):
		return self.isLive