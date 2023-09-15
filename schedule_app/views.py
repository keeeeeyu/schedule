from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import User_worktime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm


def home(request):
    return render(request, 'home.html')


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
    return render(request, 'login.html', context)


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
    if request.method == 'POST':
        last_entry = User_worktime.objects.filter(user=request.user).last()
        if last_entry.clock_in and last_entry.clock_out is not None:
            user = request.user
            clock_in_time = timezone.now()
            clocked_in = User_worktime.objects.create(user=user,clock_in=clock_in_time)
            clocked_in.save()
            messages.success(request, f'Clock-in ({clock_in_time}) successful.')
        else:
            messages.error(request, 'You are already clocked in.')
    return render(request,'home.html')

@login_required
def clock_out(request):
    if request.method == 'POST':
        last_entry = User_worktime.objects.filter(user=request.user).last()
        if last_entry.clock_out is None:
            clock_out_time = timezone.now()
            last_entry.clock_out = clock_out_time
            last_entry.save()
            messages.success(request, 'Clock-out successful.')
        else:
            messages.error(request, 'You are already clocked out.')
    return render(request,'home.html')
