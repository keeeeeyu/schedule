from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import User_worktime, User
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


def clock_in(request, user_id):
    print(user_id)


   
    
    if request.method == 'POST':
        user = request.user
        clock_in_time = timezone.now()
        clock_out_time = timezone.now()
        clocked_in = User_worktime.objects.create(user=user,clock_in=clock_in_time, clock_out=clock_out_time)
        clocked_in.save()
        print('clock in ---->', User_worktime.objects.get(clock_in))
        messages.success(request, 'Clock-in successful.')
    else:
        messages.error(request, 'You must be logged in to clock in.')
    return render(request,'home.html')