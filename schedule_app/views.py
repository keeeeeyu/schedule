from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import CreateUserForm


def home(request):
    return render(request, 'base.html')


def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        print("method is post")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'registration/signup.html', context)
