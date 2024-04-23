from django.shortcuts import render , redirect
from .models import Report
from django.http import HttpResponse
import datetime
# Create your views here.
def index(request):
	#reports = Report.objects.all()
#	return render(request,"index.html")
	return render(request , "reports.html")

def save(request):
	print(request.POST["datetime"])
	t = datetime.datetime.strptime(request.POST["datetime"],"%H:%M").time()
	print(t)
	return redirect("index")
