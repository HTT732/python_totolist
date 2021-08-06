from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Status(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['status']
    
