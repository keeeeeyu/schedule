from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    permission = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name}'


class User_worktime(models.Model):
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class User_breaktime(models.Model):
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
