from django.db import models
import pytz
from datetime import datetime, timedelta
class Report(models.Model):
    task = models.ForeignKey("Task",models.SET_NULL,null=True)
    start_time = models.DateTimeField(blank=False , null= False)
    end_time = models.DateTimeField(blank=True , null = True)
    def total_time(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        else:
            dt = datetime.now(pytz.timezone('Asia/Tehran'))
            dt_naive = dt.replace(tzinfo=None)-timedelta(hours=1)
            return dt_naive - self.start_time
class Task(models.Model):
    name = models.CharField(max_length=255,unique=True,primary_key = True)
