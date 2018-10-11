from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime


class UserManager(models.Manager):
  def validate_registration(self,post_data):
   print ("password is..**" + post_data['password'])
   print ("confirmpassword is" + post_data['confirmPW'])
   errors = []

   if len(post_data['name']) <3:
    errors.append("name must be 3 or more characters")
   #password must be 8 or more characters
   if len(post_data['password'])<8:
    errors.append("password must be 8 or more characters")
   if post_data['password'] != post_data['confirmPW']:
    errors.append("password must be same as Confirm password")
   if self.filter(username = post_data['username']):
    errors.append("username already exist")

   return errors


  def validate_addition(self,post_data):


   errors = []
   #name must be 2 or more characters
   if len(post_data['dest']) <1:
    errors.append("Destination must be entered")
   if len(post_data['desc']) <1:
    errors.append("Description must be entered")
   print ("destination done----------------")
   #password must be 8 or more characters
   return errors


  def validate_login(self,post_data):
   errors = []
   the_user = None
   if not self.filter(username = post_data['username']):
    errors.append('invalid username')
   else:
    the_user = self.get(username = post_data['username'])

    if not bcrypt.checkpw(post_data['password'].encode(), the_user.password.encode()):
     errors.append('incorrect password')
     the_user = None

   return (errors, the_user)

   #password is incorrect

  def create_user(self,clean_data):
   hashed = bcrypt.hashpw(clean_data['password'].encode(),bcrypt.gensalt())
   return self.create(
    name= clean_data['name'],
    username= clean_data['username'],
    password=hashed,
   )

  def create_trip(self,clean_data):

   return self.create(
    destination = clean_data['dest'],
    startdate = clean_data['fromDate'],
    enddate = clean_data['toDate'],
    plan = clean_data['desc'],

   )

class User(models.Model):
  name = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = UserManager()

  def __str__(self):
   return "Name: {},Username: {},".format(self.name,self.username)


class Trip(models.Model):
  destination = models.CharField(max_length=255)
  startdate = models.DateField()
  enddate = models.DateField()
  plan = models.CharField(max_length=255)
  users = models.ManyToManyField(User)
  objects = UserManager()

  def __str__(self):
   return "Destination: {}, startDate: {},enddate: {},plan: {}".format(self.destination,self.startdate,self.enddate,self.plan)
