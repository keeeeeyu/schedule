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
from datetime import datetime, date

# Create your views here.


@login_required
def home(request):
    now = datetime.now()
    date_today = now.date()
    time_now = now.strftime("%I:%M %p")
    context = {
        'time_now': time_now,
        'date_today': date_today
    }
    return render(request, 'home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            last_entry = User_worktime.objects.filter(user=request.user).last()
            current_date = date.today()
            if last_entry is not None:
                last_entry_date = last_entry.clock_in.date()
                if current_date == last_entry_date:
                    return redirect('break')
            else:
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
            clock_in_time = timezone.now()
            clocked_in = User_worktime.objects.create(
                user=user, clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({clock_in_time}) successful.')
        elif last_entry.clock_in and last_entry.clock_out is not None:
            user = request.user
            clock_in_time = timezone.now()
            clocked_in = User_worktime.objects.create(
                user=user, clock_in=clock_in_time)
            clocked_in.save()
            messages.success(
                request, f'Clock-in ({clock_in_time}) successful.')
        else:
            messages.error(request, 'You are already clocked in.')
    return render(request, 'break.html')


@login_required
def clock_out(request):
    if request.method == 'POST':
        last_entry = User_worktime.objects.filter(user=request.user).last()
        if last_entry.clock_out is None:
            clock_out_time = timezone.now()
            last_entry.clock_out = clock_out_time
            last_entry.save()
            messages.success(
                request, f'Clock-out ({clock_out_time}) successful.')
            messages.error(request, 'Error')
        else:
            messages.error(request, 'You are already clocked out.')
    return render(request, 'home.html')


@login_required
def break_time(request):
    return render(request, 'break.html')


@login_required
def break_out(request):
    # current_time = timezone.now() WHY IS THIS 7 HOURS AHEAD?????
    now = datetime.now()
    if request.method == 'POST':
        last_entry = User_breaktime.objects.filter(user=request.user).last()
        if last_entry == None:
            user = request.user
            out = timezone.now()
            break_out = User_breaktime.objects.create(
                user=user, break_out=out)
            break_out.save()
            messages.success(
                request, f'Break out ({now.time()}) successful.')
        elif last_entry.break_in == None:
            out = User_breaktime.objects.get(id=last_entry.id)
            break_in = timezone.now()
            out.break_in = break_in
            out.save()
            messages.success(
                request, f'Break in ({now.time()}) successful.')
            print("BREAK IN at", now.time())
    return render(request, 'home.html')
