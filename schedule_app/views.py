from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.utils import timezone
from .models import User_worktime, User_breaktime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta

# Create your views here.


@login_required
def home(request):
    now = timezone.localtime()
    date_today = now.date()
    time_now = now.strftime("%I:%M %p")
    context = {
        'time_now': time_now,
        'date_today': date_today
    }
    print(request.user)
    return render(request, 'home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required
def timesheets(request):
    return render(request, 'account/timesheets.html')


@login_required
def clock_in(request):
    if request.method == 'POST':
        first_entry = User_worktime.objects.filter(user=request.user).first()
        last_entry = User_worktime.objects.filter(user=request.user).last()
        print('last entry', first_entry)
        if first_entry is None:
            user = request.user
            clock_in_time = timezone.localtime()
            clocked_in = User_worktime.objects.create(
                user=user, clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({timezone.localtime(clock_in_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
        elif last_entry.clock_in and last_entry.clock_out is not None:
            user = request.user
            clock_in_time = timezone.localtime()
            clocked_in = User_worktime.objects.create(
                user=user, clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({timezone.localtime(clock_in_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
        else:
            messages.error(request, 'You are already clocked in.')
    return render(request, 'home.html')


@login_required
def clock_out(request):
    if request.method == 'POST':
        last_entry = User_worktime.objects.filter(user=request.user).last()
        if last_entry.clock_out is None:
            clock_out_time = timezone.localtime()
            last_entry.clock_out = clock_out_time
            last_entry.save()
            messages.success(
                request, f'Clock-out ({timezone.localtime(clock_out_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
        else:
            messages.error(request, 'You are already clocked out.')
    return render(request, 'home.html')


@login_required
def break_time(request):
    last_entry = User_breaktime.objects.filter(user=request.user).last()
    time_now = timezone.localtime().strftime("%I:%M %p")
    if request.method == 'POST':
        if last_entry is None or last_entry.break_out and last_entry.break_in is not None:
            user = request.user
            out = timezone.localtime()
            break_out = User_breaktime.objects.create(
                user=user, break_out=out)
            break_out.save()
            messages.success(
                request, f'Break out ({time_now}) successful.')
            return render(request, 'home.html')
        elif last_entry.break_in == None:
            out = User_breaktime.objects.get(id=last_entry.id)
            break_in = timezone.localtime()
            out.break_in = break_in
            out.save()
            print(messages)
            messages.success(
                request, f'Break in ({time_now}) successful.')
            return render(request, 'home.html')
    return render(request, 'break.html')


@login_required
def timesheets(request):
    user = request.user
    first_name = request.user.first_name.capitalize()
    last_name = request.user.last_name.capitalize()
    clock_ins = User_worktime.objects.filter(user=user).order_by(
        '-clock_in').values_list('clock_in', flat=True)
    clock_outs = User_worktime.objects.filter(user=user).order_by(
        '-clock_out').values_list('clock_out', flat=True)
    worktimes = User_worktime.objects.filter(user=user).order_by('-clock_in')
    work_hours = []
    print(work_hours)
    total_work_time = timedelta()
    for worktime in worktimes:
        if worktime.clock_out:
            time_worked = worktime.clock_out - worktime.clock_in
            hours_worked = (time_worked.total_seconds() / 3600)
            print(hours_worked)
            work_hours.append(round(hours_worked, 1))
            total_work_time += time_worked
        else:
            work_hours.append('N/A')
    total_hours = round(total_work_time.total_seconds() / 3600, 1)

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'clock_ins': clock_ins,
        'clock_outs': clock_outs,
        'total_hours': total_hours,
        'worktimes': worktimes,
        'work_hours': work_hours
    }

    return render(request, 'account/timesheets.html', context)
