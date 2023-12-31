from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('clock/', views.clock, name='clock'),
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('timesheets/<int:employee_id>/<str:start_date>/<str:end_date>',
         views.timesheets, name='timesheets'),
    path('break_time/', views.break_time, name='break_time'),
    path('employees/', views.all_employees, name='all_employees'),
    path('employees/<int:employee_id>',
         views.show_employee, name='show_employee'),
    path('employees/<int:employee_id>/',
         views.pick_date_range, name='pick_date_range'),
    path('account/profile/', views.profile, name='profile'),
    path('account/edit_profile/', views.edit_profile, name='edit_profile'),
    path('account/profile/<int:employee_id>/update_profile',
         views.update_profile, name='update_profile'),
    path('schedule/create_shift/', views.create_shift, name='create_shift'),
    path('schedule/add_shift/', views.add_shift, name='add_shift'),
    path('schedule/', views.getAllShifts, name='get_all_shifts'),
    path('api_call/', views.api_call, name='api_call'),
]
