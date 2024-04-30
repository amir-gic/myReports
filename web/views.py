from django.shortcuts import render , redirect
from .models import Report , Task
from django import forms
from django.http import HttpResponse
from datetime import datetime , date , time
# Create your views here.
def index(request):
	tasks = Task.objects.all()
	names = [t.name for t in tasks]
	reports = Report.objects.filter(start_time__gte = date.today())
	#reports = Report.objects.all()
	#return render(request,"index.html")
	return render(request , "reports.html" , {"tasks":names , "reports":reports})

def save(request):
	post = request.POST.copy()
	post["start_time"] =	datetime.combine(date.today() , datetime.strptime(request.POST["start_time"],"%H:%M").time())
	form = ReportForm(post)
	if form.is_valid():
		form.save()
		reports = Report.objects.all()
		if(len(reports) > 1):
			latest_report = reports[len(reports) - 2]
			latest_report.end_time = post["start_time"]
			latest_report.save()
	else:
		print("inValid")
	
	return redirect("index")


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = ['task', 'start_time' , 'end_time']