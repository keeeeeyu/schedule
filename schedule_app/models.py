from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class User_worktime(models.Model):
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class User_breaktime(models.Model):
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
