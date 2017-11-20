from django.db import models

# Create your modelss here.
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

	def __str__(self):
		return self.timestamp