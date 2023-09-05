from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.returnRegisterPage, name='register'),
    path('signup', views.signup, name='signup'),
]
