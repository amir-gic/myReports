from django.db import models

class Report(models.Model):
    task = models.ForeignKey("Task",models.SET_NULL,null=True)
    start_time = models.DateTimeField(blank=False , null= False)
    end_time = models.DateTimeField(blank=True , null = True)
    def total_time(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        else:
            return None
class Task(models.Model):
    name = models.CharField(max_length=255,unique=True,primary_key = True)
