from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.utils import timezone
from .models import User_worktime, User_breaktime, User_schedule, DEPARTMENTS
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.conf import settings
import requests
from geopy.distance import geodesic

# Create your views here.
# def get_user_location(request, latitude, longitude):
#     print(latitude, longitude,'get user locatino check')
#     target_latitude = settings.TARGET_LOCATION['latitude']
#     target_longitude = settings.TARGET_LOCATION['longitude']

#     if user_latitude is not None and user_longitude is not None:
#             try:
#                 user_latitude = float(user_latitude)
#                 user_longitude = float(user_longitude)
#                 print(user_latitude, 'checking if statement')
#             except ValueError:
#                 # Handle the case where latitude or longitude is not a valid float
#                 return False  # or handle it according to your requirements
#             is_within_radius_result = is_within_radius(user_latitude, user_longitude, target_latitude, target_longitude)
            
#             return is_within_radius_result
#     return JsonResponse({'latitude': latitude, 'longitude': longitude})

    

# def is_within_radius(user_latitude, user_longitude, target_latitude, target_longitude):
#     print('is within radius')
#     user_location = (user_latitude, user_longitude)
#     target_location = (target_latitude, target_longitude)
#     distance = geodesic(user_location, target_location).miles
#     return distance <= 10


def calculate_week_dates(date_today, day_count):
    start_of_week = date_today - timedelta(days=date_today.weekday())
    week_dates = [start_of_week +
                  timedelta(days=day_count + i) for i in range(7)]
    return week_dates

def api_call(request):
    if request.method == 'GET':
        try:
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')
            print(latitude,longitude)
            # Call the geocoding API
            api_key = settings.MAPQUEST_API_KEY
            api_url = f'https://www.mapquestapi.com/geocoding/v1/reverse?key={api_key}&location={latitude},{longitude}&includeRoadMetadata=true&includeNearestIntersection=true'
            
            response = requests.get(api_url)
            data = response.json()

            # Extract city and state information from the geocoding API response
            city = data['results'][0]['locations'][0]['adminArea5']
            state = data['results'][0]['locations'][0]['adminArea3']

            # Send the city and state information as JSON response
            return JsonResponse({'city': city, 'state': state})

        except Exception as e:
            print('Error:', e)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def home(request):
    first_name = request.user.first_name.capitalize()
    now = timezone.localtime()
    date_today = now.date()
    time_now = now.strftime("%I:%M %p")
    start_of_week = date_today - timedelta(days=date_today.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    day_count = request.session.get('day_count', 0)
    
    if request.method == "POST":
        if 'next_week' in request.POST:
            request.session['day_count'] = day_count + 7
            day_count = request.session['day_count']
            next_week = date_today + timedelta(days=day_count)
            start_of_week = next_week - timedelta(days=next_week.weekday())
            week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        elif 'past_week' in request.POST:
            request.session['day_count'] = day_count - 7
            day_count = request.session['day_count']
            next_week = date_today + timedelta(days=day_count)
            start_of_week = next_week - timedelta(days=next_week.weekday())
            week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        elif 'current_week' in request.POST:
            request.session['day_count'] = 0
    else:
        request.session['day_count'] = 0

    shifts = getAllShifts()
    print(shifts)

    context = {
        'time_now': time_now,
        'date_today': date_today,
        'first_name': first_name,
        'week_dates': week_dates,
    }
    return render(request, 'home.html', context)


def getAllShifts():
    shifts = User_schedule.objects.all()
    return shifts


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
def clock(request):
    first_name = request.user.first_name.capitalize()
    user_worktime = User_worktime.objects.filter(user=request.user).last()
    user_breaktime = User_breaktime.objects.filter(user=request.user).last()
    now = timezone.localtime()
    date_today = now.date()
    hours_worked = timedelta()
    hours_break = timedelta()

    if user_breaktime is not None:
        if date_today == user_breaktime.break_in.date():
            break_in_time = user_breaktime.break_in
            if user_breaktime.break_out is None:
                break_out_time = None
                hours_break = 0
            else:
                break_out_time = user_breaktime.break_out
                break_time = break_out_time - break_in_time
                hours_break = round(break_time.total_seconds() / 3600, 2)
        elif user_breaktime.break_out is not None:
            break_out_time = user_breaktime.break_out
            break_in_time = user_breaktime.break_in
            break_time = break_out_time - break_in_time
            hours_break = round(break_time.total_seconds() / 3600, 2) 
        else:
            break_in_time = None
            break_out_time = None
            hours_break = 0
    else:
        break_in_time = None
        break_out_time = None
        hours_break = 0
        

    if user_worktime is not None:
        clock_in_verification = user_worktime.clock_out is not None
        clock_in_time = user_worktime.clock_in
        clock_out_time = user_worktime.clock_out
        hours_worked = 0
        if date_today == clock_in_time.date():
            if user_worktime.clock_out is None:
                time_worked = now - clock_in_time
                hours_worked = round(time_worked.total_seconds() / 3600, 2)
            else:
                time_worked = clock_out_time - clock_in_time
                hours_worked = round(time_worked.total_seconds() / 3600, 2)
        elif user_worktime.clock_out is None:
            time_worked = now - clock_in_time
            hours_worked = round(time_worked.total_seconds() / 3600, 2)
        elif user_worktime.clock_out is not None:
            time_worked = clock_out_time - clock_in_time
            hours_worked = round(time_worked.total_seconds() / 3600, 2) 
    else:
        clock_in_verification = True
        hours_worked = 0
        clock_in_time = None
        clock_out_time = None
    print(hours_worked, hours_break)
    
    net_hours_worked = round((hours_worked - hours_break), 2)

    context = {
        'first_name': first_name,
        'clock_in_verification': clock_in_verification,
        'hours_worked': hours_worked,
        'date_today': date_today,
        'now': now,
        'clock_in_time': clock_in_time,
        'clock_out_time': clock_out_time,
        'break_in_time': break_in_time,
        'break_out_time': break_out_time,
        'net_hours_worked': net_hours_worked,
    }

    return render(request, 'clock.html', context)


@login_required
def clock_in(request):
    if request.method == 'POST':
            user_location = request.POST.get('user_location', None)
            print(user_location)

            if user_location:
                target_location = (settings.TARGET_LOCATION['latitude'], settings.TARGET_LOCATION['longitude'])
                print('check 2')
                user_location = tuple(map(float, user_location.split(',')))
                distance_to_target = geodesic(user_location, target_location).miles
                if distance_to_target <= 10.0:
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
                else:
                    messages.error(request, 'You are not within the allowed radius to clock in.')
            else:
                messages.error(request, 'Unable to retrieve your location. Make sure location services are enabled.')
                
    return redirect('clock')


@login_required
def clock_out(request):
    if request.method == 'POST':
        user_location = request.POST.get('user_location', None) 
        last_entry = User_worktime.objects.filter(user=request.user).last()
        if user_location:
            target_location = (settings.TARGET_LOCATION['latitude'], settings.TARGET_LOCATION['longitude'])
            print('check 2')
            user_location = tuple(map(float, user_location.split(',')))
            distance_to_target = geodesic(user_location, target_location).miles
            if distance_to_target <= 10.0:
                if last_entry.clock_out is None:
                    clock_out_time = timezone.localtime()
                    last_entry.clock_out = clock_out_time
                    last_entry.save()
                    messages.success(
                        request, f'Clock-out ({timezone.localtime(clock_out_time).strftime("%Y-%m-%d %H:%M:%S")}) successful.')
                else:
                    messages.error(request, 'You are already clocked out.')
            else:
                messages.error(request, 'You are not within the allowed radius to clock out.')
        else:
            messages.error(request, 'Unable to retrieve your location. Make sure location services are enabled.')

    return redirect('clock')


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
            break_in = User_breaktime.objects.create(
                user=user, date=datetime.now(), break_in=out)
            break_in.save()
            messages.success(
                request, f'Break in ({time_now}) successful.')
            return redirect('clock')
        elif last_entry.break_out == None:
            out = User_breaktime.objects.get(id=last_entry.id)
            break_out = timezone.localtime()
            out.break_out = break_out
            out.save()
            print(messages)
            messages.success(
                request, f'Break out ({time_now}) successful.')
            return redirect('clock')
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
    first_name = request.user.first_name.capitalize() 
    employee = User.objects.get(id=employee_id)
    return render(request, 'account/employee.html', {'employee': employee, 'first_name': first_name})


@ login_required
def pick_date_range(request, employee_id):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    return redirect(f'/timesheets/{employee_id}/{start_date}/{end_date}')


@login_required
def create_shift(request):
    all_employees = User.objects.all().values()
    departments = DEPARTMENTS

    context = {
        'all_employees': all_employees,
        'departments': departments,
    }
    return render(request, 'schedule/add_shift.html', context)


@ login_required
def add_shift(request):

    shift = User_schedule.objects.create(
        date=request.POST.get('date'),
        user_id=request.POST.get('user'),
        start_time=request.POST.get('start_time'),
        end_time=request.POST.get('end_time'),
        department=request.POST.get('department')
    )
    shift.save()
    return render(request, 'schedule/add_shift.html')


@ login_required
def profile(request):
    first_name = request.user.first_name.capitalize()
    user = request.user

    user_values = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'staff_status': user.is_superuser,
        'date_joined': user.date_joined
    }

    context = {
        'first_name': first_name,
        'user_values': user_values
    }

    return render(request, 'account/profile.html', context)


def edit_profile(request):
    first_name = request.user.first_name.capitalize()
    return render(request, 'account/edit_profile.html', {'first_name': first_name})


def is_username_taken(username):
    return User.objects.filter(username=username).exists()


@ login_required
def update_profile(request, employee_id):
    try:
        user_profile = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        # Handle the case where the user with the specified user_id does not exist
        return render(request, 'user_not_found.html')

    user_profile = User.objects.get(id=employee_id)
    username = request.POST.get('username', user_profile.username)
    first_name = request.POST.get('first_name', user_profile.first_name)
    last_name = request.POST.get('last_name', user_profile.last_name)
    email = request.POST.get('email', user_profile.email)
    current_password = request.POST.get('current_password', user_profile.password)
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if username != user_profile.username and is_username_taken(username):
        messages.error(
            request, 'Username is already taken. Please choose a different username.')
        return render(request, 'account/edit_profile.html',  {'error_message': 'Username is already taken. Please choose a different username.'})

    user_profile.username = username
    user_profile.first_name = first_name
    user_profile.last_name = last_name
    user_profile.email = email

    if current_password and new_password and confirm_password:
        if user_profile.check_password(current_password):
            if new_password == current_password:
                messages.error(request, 'Your new password must be different from your current password')
                return render(request, 'account/edit_profile.html', {'error_message': 'Your new password must be different from your current password'})
            if new_password == confirm_password:
                user_profile.set_password(new_password)
                update_session_auth_hash(request, user_profile)
            else:
                messages.error(request, 'New password and confirm password must match.')
                return render(request, 'account/edit_profile.html', {'error_message': 'New password and confirm password must match.'})
        else:
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'account/edit_profile.html', {'error_message': 'Current password is incorrect.'})
        
    user_profile.save()
    return redirect('profile')
