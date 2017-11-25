#from django.shortcuts import render
from django.http import JsonResponse, HttpResponse 
from django.shortcuts import render
from django.core.files import File
import os

from .models import Telemetry

# Create your views here.
def index(request):
	return render(request, 'testGraph/index.html', {'telemetry': Telemetry.objects.get(id=2)})

def onegraph(request):
	return render(request, 'testGraph/onegraph.html')

def twograph(request):
	return render(request, 'testGraph/twograph.html', {
		'telemetry': Telemetry.objects.all(),
		})

def testing(request):
	return HttpResponse("<b>More testing here</b>")

# getdata(request, sensor)
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








	#load static
	#stuff = static "testGraph/turntable-1.txt"
	#return HttpResponse(stuff)
	#http://127.0.0.1:8000/static/testGraph/turntable-1.txt
	#need to parse instead of hardcoding file path
	'''
	filepath = "/Users/karthikpullela/Desktop/Django-projects/Reach-Sentinel-Lite/reachSentinelLite/testGraph/static/testGraph/turntable-1.txt"
	result = "Initial---"
	if (os.path.exists(filepath)):
		result += " true"
		hello = File.open("./static/testGraph/turntable-1.txt")
		for line in File:
			result += line + "<br>"
		File.close()
		


	return HttpResponse(result)
	#return HttpResponse(os.path.realpath(__file__))

'''