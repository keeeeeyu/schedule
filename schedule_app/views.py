from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.utils import timezone
from .models import User_worktime, User_breaktime, User_schedule
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime


# Create your views here.


@login_required
def home(request):
    first_name = request.user.first_name.capitalize()
    now = timezone.localtime()
    date_today = now.date()
    time_now = now.strftime("%I:%M %p")
    context = {
        'time_now': time_now,
        'date_today': date_today,
        'first_name': first_name
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
def clock_in(request):
    first_name = request.user.first_name.capitalize()
    if request.method == 'POST':
        first_entry = User_worktime.objects.filter(user=request.user).first()
        last_entry = User_worktime.objects.filter(user=request.user).last()
        print('last entry', first_entry)
        if first_entry is None:
            user = request.user
            clock_in_time = timezone.localtime()
            clocked_in = User_worktime.objects.create(
                user=user, date=datetime.now(), clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({timezone.localtime(clock_in_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
        elif last_entry.clock_in and last_entry.clock_out is not None:
            user = request.user
            clock_in_time = timezone.localtime()
            clocked_in = User_worktime.objects.create(
                user=user, date=datetime.now(), clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({timezone.localtime(clock_in_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
        else:
            messages.error(request, 'You are already clocked in.')
    return render(request, 'home.html', {'first_name': first_name})


@login_required
def clock_out(request):
    first_name = request.user.first_name.capitalize()
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
    return render(request, 'home.html', {'first_name': first_name})


@login_required
def break_time(request):
    first_name = request.user.first_name.capitalize()
    last_entry = User_breaktime.objects.filter(user=request.user).last()
    time_now = timezone.localtime().strftime("%I:%M %p")
    if request.method == 'POST':
        if last_entry is None or last_entry.break_out and last_entry.break_in is not None:
            user = request.user
            out = timezone.localtime()
            print(datetime.now(), "LOOOOOK")
            break_out = User_breaktime.objects.create(
                user=user, date=datetime.now(), break_out=out)
            break_out.save()
            messages.success(
                request, f'Break out ({time_now}) successful.')
            return render(request, 'home.html', {'first_name': first_name})
        elif last_entry.break_in == None:
            out = User_breaktime.objects.get(id=last_entry.id)
            break_in = timezone.localtime()
            out.break_in = break_in
            out.save()
            print(messages)
            messages.success(
                request, f'Break in ({time_now}) successful.')
            return render(request, 'home.html', {'first_name': first_name})
    return render(request, 'break.html', {'first_name': first_name})


@login_required
def timesheets(request, employee_id, start_date, end_date):
    employee = User.objects.get(id=employee_id)
    first_name = employee.first_name.capitalize()
    last_name = employee.last_name.capitalize()

    worktimes = User_worktime.objects.filter(
        user=employee, date__gte=start_date, date__lte=end_date).order_by('-clock_in')
    clock_ins = worktimes.filter(user=employee).order_by(
        '-clock_in').values_list('clock_in', flat=True)
    clock_outs = worktimes.filter(user=employee).order_by(
        '-clock_out').values_list('clock_out', flat=True)

    work_hours = []
    total_work_time = timedelta()
    for worktime in worktimes:
        if worktime.clock_out:
            time_worked = worktime.clock_out - worktime.clock_in
            hours_worked = (time_worked.total_seconds() / 3600)
            work_hours.append(round(hours_worked, 1))
            total_work_time += time_worked
        else:
            work_hours.append('N/A')
    total_work_hours = round(total_work_time.total_seconds() / 3600, 1)

    breaktimes = User_breaktime.objects.filter(
        user=employee, date__gte=start_date, date__lte=end_date).order_by('-break_out')
    break_outs = breaktimes.filter(user=employee).order_by(
        '-break_out').values_list('break_out', flat=True)
    break_ins = breaktimes.filter(user=employee).order_by(
        '-break_in').values_list('break_in', flat=True)

    break_periods = []
    for x, y in zip(break_outs, break_ins):
        break_periods.append(
            f'{x.strftime("%I:%M")} - {y.strftime("%I:%M")}')

    break_hours = []
    total_break_time = timedelta()
    for breaktime in breaktimes:
        if breaktime.break_in:
            break_period = breaktime.break_in - breaktime.break_out
            hours_break = (break_period.total_seconds() / 3600)
            break_hours.append(round(hours_break, 1))
            total_break_time += break_period
        else:
            break_hours.append('N/A')
    total_break_hours = round(total_break_time.total_seconds() / 3600, 1)

    net_hours = total_work_hours - total_break_hours

    regular_hours = []
    for x, y in zip(work_hours, break_hours):
        regular_hours.append(x-y)

    context = {
        'id': employee.id,
        'first_name': first_name,
        'last_name': last_name,
        'clock_ins': clock_ins,
        'clock_outs': clock_outs,
        'total_work_hours': total_work_hours,
        'break_periods': break_periods,
        'net_hours': net_hours,
        'regular_hours': regular_hours,
    }

    return render(request, 'account/timesheets.html', context)


@ login_required
def all_employees(request):
    users = User.objects.all().values()
    context = {
        'employees': users
    }
    return render(request, 'all_employees.html', context)


@ login_required
def show_employee(request, employee_id):
    employee = User.objects.get(id=employee_id)
    return render(request, 'account/employee.html', {'employee': employee})


@ login_required
def pick_date_range(request, employee_id):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    return redirect(f'/timesheets/{employee_id}/{start_date}/{end_date}')
