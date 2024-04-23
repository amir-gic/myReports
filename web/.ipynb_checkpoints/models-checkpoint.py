from django.db import models

class Report(models.Model):
	task = models.F
	time = models.TimeField()
	description = models.TextField()

class Task(models.Model):
    name = models.CharField(max_length=255,unique=True,primary_key = True)
    
