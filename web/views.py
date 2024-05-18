from django.shortcuts import render , redirect
from .models import Report , Task
from django import forms
from django.http import HttpResponse
from datetime import datetime , date , time
from .converters import DateTimeRange
# Create your views here.
def index(request):
	tasks = Task.objects.all()
	names = [t.name for t in tasks]
	reports = Report.objects.filter(start_time__gte = date.today())
	reports = sorted(reports , key = lambda x : x.start_time)

	today = DateTimeRange.today()
	#reports = Report.objects.all()
	#return render(request,"index.html")
	return render(request , "reports.html" , {"tasks":names , "reports":reports , "today":today})

def save(request):
	post = request.POST.copy()
	post["start_time"] =	datetime.combine(date.today() , datetime.strptime(request.POST["start_time"],"%H:%M").time())
	if Report.objects.filter(start_time__gte = date.today()).filter(start_time__gte = post["start_time"]).exists():
		return HttpResponse("error")
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

def detail(request , timerange:DateTimeRange):
	return HttpResponse(timerange.range)

def add_task(request):
	if request.method == "POST":
		form = TaskForm(request.POST)
		form.save()
		return redirect("index")
	else:
		return render(request,"add_task.html")

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['name']

def delete_task(request):
	if request.method == "POST":
		Task.objects.filter(pk = request.POST["name"]).delete()
		return redirect("index")
	else:
		tasks = Task.objects.all()
		names = [t.name for t in tasks]
		return render(request , "delete_task.html" ,{"tasks":names})
	
def delete_reprot(request,pk):
	selectet = Report.objects.get(pk = pk)
	if selectet == Report.objects.last():
		selectet.delete()
		last = Report.objects.last()
		if last != None:
			last.end_time = None
			last.save()
	else:
		selectet.delete()
		befor = Report.objects.filter(pk__lt = pk).last()
		after = Report.objects.filter(pk__gt = pk).first()
		befor.end_time = after.start_time
		befor.save()
	Report.objects.last()
	return redirect("index")
	
