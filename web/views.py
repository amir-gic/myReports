from django.shortcuts import render , redirect
from .models import Report , Task
from django import forms
from django.http import HttpResponse
from datetime import datetime , timedelta
from .converters import DateTimeRange
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
import pytz
from repots.settings import TIME_ZONE
# Create your views here.
def index(request):
	tasks = Task.objects.all()
	names = [t.name for t in tasks]
	reports = Report.objects.filter(start_time__gte = timezone.localtime().date())
	reports = sorted(reports , key = lambda x : x.start_time)

	today = DateTimeRange.today()
	#reports = Report.objects.all()
	#return render(request,"index.html")
	return render(request , "reports.html" , {"tasks":names , "reports":reports , "today":today})

def save(request):
	post = request.POST.copy()
	today = timezone.localtime().date()
	combined_time = datetime.combine(today,datetime.strptime(request.POST["start_time"],"%H:%M").time())
	post["start_time"] = pytz.timezone(TIME_ZONE).localize(combined_time)
	if Report.objects.filter(start_time__gte = today).filter(start_time__gte = post["start_time"]).exists():
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
	if timerange.range == "day":
		reports =  Report.objects.filter(start_time__date = timerange.make_date())
		tottal_times = {}
		for i in Task.objects.all():
			tottal_times[i] = timedelta(0)
			for j in reports.filter(task = i):
				tottal_times[i] = tottal_times[i] + j.total_time()
		tottal_times = sorted(tottal_times.items() , key = lambda x : x[1] , reverse= True )
		reports = sorted(reports , key = lambda x : x.start_time)
		tasks_names = [task[0].name for task in tottal_times]
		tasks_vals = [task[1].total_seconds() for task in tottal_times]
		return render(request , "detail.html", {"tasks_data":tottal_times  , 'tasks_names': mark_safe(json.dumps(tasks_names)) , 'tasks_vals': mark_safe(json.dumps(tasks_vals))})

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
	
