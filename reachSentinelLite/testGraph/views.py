#from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'testGraph/index.html')

def testing(request):
	return HttpResponse("<b>More testing here</b>")