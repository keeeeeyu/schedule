from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('home/', views.clock_in, name='clock_in'),
]
