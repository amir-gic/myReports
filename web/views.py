from django.shortcuts import render , redirect
from .models import Report , Task
from django import forms
from django.http import HttpResponse
from datetime import datetime , date , time
# Create your views here.
def index(request):
	tasks = Task.objects.all()
	names = [t.name for t in tasks]
	reports = Report.objects.filter(time__gte = date.today())
	#reports = Report.objects.all()
#	return render(request,"index.html")
	return render(request , "reports.html" , {"tasks":names , "reports":reports})

def save(request):
	post = request.POST.copy()
	post["start_time"] =	datetime.combine(date.today() , datetime.strptime(request.POST["start_time"],"%H:%M").time())
	print(post)
	form = ReportForm(post)
	if form.is_valid():
		form.save()
		latest_report = Report.objects.all()
		latest_report = latest_report[len(latest_report) - 2]
		latest_report.end_time = datetime.now()
		latest_report.save()
	else:
		print("inValid")
	# t = datetime.datetime.strptime(request.POST["time"],"%H:%M").time()
	# print(t)
	return redirect("index")


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = ['task', 'start_time']