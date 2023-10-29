from django.contrib import admin

# Register your models here.
from .models import User_worktime, User_breaktime, User_schedule

# admin.site.register(User)
admin.site.register(User_worktime)
admin.site.register(User_breaktime)
admin.site.register(User_schedule)
