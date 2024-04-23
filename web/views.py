from django.shortcuts import render , redirect
from .models import Report , Task
from django import forms
from django.http import HttpResponse
from datetime import datetime , date , time
# Create your views here.
def index(request):
	tasks = Task.objects.all()
	names = [t.name for t in tasks]
	reports = Report.objects.all()
	#reports = Report.objects.all()
#	return render(request,"index.html")
	return render(request , "reports.html" , {"tasks":names , "reports":reports})

def save(request):
	post = request.POST.copy()
	post["time"] =	datetime.combine(date.today() , datetime.strptime(request.POST["time"],"%H:%M").time())
	print(post)
	form = ReportForm(post)
	if form.is_valid():
		form.save()
	else:
		print("inValid")
	# t = datetime.datetime.strptime(request.POST["time"],"%H:%M").time()
	# print(t)
	return redirect("index")


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = ['task', 'time']