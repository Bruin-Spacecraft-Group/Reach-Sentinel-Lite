from graphs.models import Telemetry


Telemetry.objects.create(
timestamp = 60000, 
accel_x   = 8, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 74)

Telemetry.objects.create(
timestamp = 120000, 
accel_x   = 7, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 75)

Telemetry.objects.create(
timestamp = 180000, 
accel_x   = 10, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 72)

Telemetry.objects.create(
timestamp = 240000, 
accel_x   = 4, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 76)

Telemetry.objects.create(
timestamp = 300000, 
accel_x   = 16, 
accel_y   = 16, 
accel_z   = 256, 
gyro_x    = -86, 
gyro_y    = -62, 
gyro_z    = 69,
barometer = 99420,
temp      = 72)







#Telemetry.save()
