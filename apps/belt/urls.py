from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.travels_add),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^add/trip$', views.add_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
]