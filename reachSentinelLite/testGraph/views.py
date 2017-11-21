#from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render
from django.core.files import File
import os

# Create your views here.
def index(request):
	return render(request, 'testGraph/index.html')

def onegraph(request):
	return render(request, 'testGraph/onegraph.html')

def testing(request):
	return HttpResponse("<b>More testing here</b>")

def getdata(request):

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