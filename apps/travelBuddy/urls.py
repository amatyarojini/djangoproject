from django.conf.urls import url
from . import views

urlpatterns = [
 url(r'^main$',views.index),
 url(r'^main/register$',views.register),
 url(r'^main/login$',views.login),
 url(r'^travels$',views.travels),
 url(r'^travels/add$',views.addPlan),
 url(r'^travels/addProcess$',views.addProcess),
  url(r'^travels/destination/(?P<id>\d+)$', views.destination_info),



]
