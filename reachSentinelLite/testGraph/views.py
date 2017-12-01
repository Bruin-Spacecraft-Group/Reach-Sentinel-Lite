from django.http import JsonResponse, HttpResponse 
from django.shortcuts import render
from django.core.files import File
import os

from .models import Telemetry

# Create your views here.
def index(request):
	return render(request, 'testGraph/index.html')

def onegraph(request):
	return render(request, 'testGraph/onegraph.html')

def twograph(request):
	return render(request, 'testGraph/twograph.html', {
		'telemetry': Telemetry.objects.all(),
		})

def testing(request):
	return HttpResponse("<b>More testing here</b>")

# getdata(request, sensor)
# or we could get all the data, then get the specifics within app
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

		data[i] = [aa[0], aa[int(sensor)]]
		i = i + 1
	return JsonResponse({'stuff': data})