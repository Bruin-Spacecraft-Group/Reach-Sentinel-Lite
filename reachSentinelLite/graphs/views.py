from django.shortcuts import render

from .models import Telemetry

# Create your views here.
def index(request):
	return render(request, 'graphs/index.html')


# we could get individual columns at a time
# this way, we don't have to worry about creating multiple instances of function
# usage: var data = [data[timestamp], data[sensor-1], data[sensor-2]]
def getdata(request):
	data = [None] * Telemetry.objects.count()
	i = 0
	for x in Telemetry.objects.all():
		# Need to find a way to use iterator
		aa = [None] * 9
		aa[0] = x.timestamp
		aa[1] = x.accel_x
		aa[2] = x.accel_y
		aa[3] = x.accel_z
		aa[4] = x.gyro_x
		aa[5] = x.gyro_y
		aa[6] = x.gyro_z
		aa[7] = x.barometer
		aa[8] = x.temp

		data[i] == aa;
		i = i + 1
	return JsonResponse({'stuff': data})

def getdata(request, sensor):
	data = [None] * Telemetry.objects.count()
	i = 0
	for x in Telemetry.objects.all():
		# Need to find a way to use iterator
		aa = [None] * 9
		aa[0] = x.timestamp
		aa[1] = x.accel_x
		aa[2] = x.accel_y
		aa[3] = x.accel_z
		aa[4] = x.gyro_x
		aa[5] = x.gyro_y
		aa[6] = x.gyro_z
		aa[7] = x.barometer
		aa[8] = x.temp

		data[i] = [aa[0], aa[int(sensor)], aa[int(sensor+1)]]
		i = i + 1
	return JsonResponse({'stuff': data})
