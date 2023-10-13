from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class User_worktime(models.Model):
    date = models.DateField(null=True, blank=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.clock_in}'


class User_breaktime(models.Model):
    date = models.DateField(null=True, blank=True)
    break_out = models.DateTimeField(null=True, blank=True)
    break_in = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.break_out}'
