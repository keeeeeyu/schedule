from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'base.html')

def signup(request):
    return render(request, 'registration/signup.html')