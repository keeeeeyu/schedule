from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

DEPARTMENTS = (
    ('P', 'Pharmacist'),
    ('R', 'Retail'),
    ('O', 'Office'),
    ('F', 'Filling'),
    ('D', 'Dispatch'),
    ('D/F', 'Dispatch/Filling'),
    ('C', 'Compounding'),
    ('DME', 'DME Driver'),
    ('DE', 'Data Entry'),
    ('W', 'Warehouse')
)


class User_worktime(models.Model):
    date = models.DateField(null=True, blank=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user}: {self.clock_in}-{self.clock_out}'


class User_breaktime(models.Model):
    date = models.DateField(null=True, blank=True)
    break_out = models.DateTimeField(null=True, blank=True)
    break_in = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user}: {self.break_out}-{self.break_in}'


class User_schedule(models.Model):
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_time = models.CharField(null=True, blank=True, max_length=10)
    end_time = models.CharField(null=True, blank=True, max_length=10)
    department = models.CharField(
        max_length=3, choices=DEPARTMENTS, default=DEPARTMENTS[0][0])

    def __str__(self):
        return f'{self.user}: {self.start_time}-{self.end_time}'
