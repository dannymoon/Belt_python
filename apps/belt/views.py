from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'belt/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_password)
            messages.error(request, "Successfully Registered")
            return redirect('/')

def login(request):
    if request.method == 'POST':
        if not 'login_status' in request.session:
            request.session['login_status'] = False
        login_data = User.objects.filter(username=request.POST['username'])
        if len(request.POST['username']) < 1:
            messages.error(request, "enter username")
            return redirect('/')
        if len(request.POST['password']) < 1:
            messages.error(request, "enter password")
            return redirect('/')
        inputted_password = request.POST['password']
        stored_password = User.objects.filter(username=request.POST['username']).first().password
        if login_data and bcrypt.checkpw(inputted_password.encode(), stored_password.encode()):
            request.session['login_status'] = {'id':login_data.first().id, 'name':login_data.first().name, 'username':login_data.first().username}
            return redirect('/travels')
        else:
            messages.error(request, "Username and password does not match")
            return redirect('/')    

def logout(request):
    request.session['login_status'] = False
    return redirect('/')

def travels(request):
    if 'login_status' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['login_status']['id'])
    context = {
        'user': this_user,
        'your_trips': Trip.objects.filter(trip_joiners=this_user),
        'other_trip': Trip.objects.exclude(trip_joiners=this_user)
    }
    return render(request, 'belt/travels.html', context)

def travels_add(request):
    return render(request, 'belt/add.html')

def home(request):
    return redirect('/travels')

def destination(request, trip_id):
    context = {
        'trip' : Trip.objects.get(id=trip_id),
        'trip_joiners' : User.objects.filter(trips_going__id=trip_id).exclude(trip_made__id=trip_id),
    }
    return render(request, 'belt/destination.html', context)

def add_trip(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/travels/add')
        else:
            this_user = User.objects.get(id=request.session['login_status']['id'])
            Trip.objects.create(
                destination=request.POST['destination'],
                description=request.POST['description'],
                travel_date_from=request.POST['travel_date_from'],
                travel_date_to=request.POST['travel_date_to'],
                trip_maker=this_user
            )
    
            Trip.objects.get(
                destination=request.POST['destination'], 
                description=request.POST['description'], 
                travel_date_from=request.POST['travel_date_from'],
                travel_date_to=request.POST['travel_date_to'],
                trip_maker=this_user
            ).trip_joiners.add(this_user)
            return redirect('/travels')

def join(request, trip_id):
    this_user = User.objects.get(id=request.session['login_status']['id'])
    Trip.objects.get(id=trip_id).trip_joiners.add(this_user)
    return redirect('/travels')