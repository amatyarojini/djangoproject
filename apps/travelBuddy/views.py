from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages


# Create your views here.
def index(request):
  return render(request, 'travelBuddy/index.html')

def register(request):
  print("inside register")
  print (request.POST)
  errs = User.objects.validate_registration(request.POST)
  if errs:
   for e in errs:
    messages.error(request,e)
  else:
   #create user
   new_user = User.objects.create_user(request.POST)
   request.session['id'] = new_user.id
   messages.success(request,"Thank you {} for regestering".format(new_user.name))
  return redirect('/main')


def login(request):
 print("inside login")
 result = User.objects.validate_login(request.POST)
 if result[0]:
  for e in result[0]:
   messages.error(request,e)
   return redirect('/main')

 else:
  request.session['id'] = result[1].id
  request.session['username'] = result[1].username
  messages.success(request,"Welcome {}".format(result[1].username))
  return redirect('/travels')

def travels(request):
 users = User.objects.all()
 print("inside travels")
 id = request.session['id']
 trips =User.objects.get(id =id).trip_set.all()
 trip2 = Trip.objects.all()#Trip.objects.exclude(users__id = id)

 context = {
  'all_trips': trips,
  'trip_two' : trip2,
  'all_users': users,
 }
 return render(request,'travelBuddy/travels.html',context)


def addPlan(request):
 return render(request,'travelBuddy/addPlan.html')

def addProcess(request):
  print (request.POST)
  errs = User.objects.validate_addition(request.POST)

  if errs:
   for e in errs:
    messages.error(request,e)
  else:

    #create user
    new_trip = Trip.objects.create_trip(request.POST)
    messages.success(request,"Thank you for adding trip")
    return redirect('/travels')


def destination_info(request,id):
 trip_id = request.GET['trip_id']
 otherusers = Trip.objects.get(id = trip_id).users.exclude(id = id)
 users = User.objects.all()
 user = User.objects.get(id = id)
 trips =User.objects.get(id =id).trip_set.all()
 context = {
  'Trips': trips,
  'User': user,
  'id': id,
  'all_users': users,
  'other_users': otherusers,
 }
 return render(request,'travelBuddy/destination_info.html',context)
