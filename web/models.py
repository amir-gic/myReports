from django.db import models

class Report(models.Model):
    task = models.ForeignKey("Task",models.SET_NULL,null=True)
    time = models.DateTimeField(blank=False , null= False)

class Task(models.Model):
    name = models.CharField(max_length=255,unique=True,primary_key = True)
