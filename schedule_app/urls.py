from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('timesheets/', views.timesheets, name='timesheets'),
    path('break_time/', views.break_time, name='break'),
    path('break_out/', views.break_out, name='break_out'),
]
