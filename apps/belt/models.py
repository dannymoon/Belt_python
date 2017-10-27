from __future__ import unicode_literals
from django.db import models
import re
import datetime

# Create your models here.
nameREGEX = re.compile(r'^[A-Za-z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1 or len(postData['username']) < 1 or len(postData['password']) < 1 or len(postData['confirm_password']) < 1:
            errors["all"] = "All fields must be filled"
            return errors
        if len(postData['name']) < 3:
            errors["name"] = "Name should be more than 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username should be more than 3 characters"
        if not nameREGEX.match(postData['name']):
            errors["name"] = "name fields must be letter characters only"
        if not nameREGEX.match(postData['username']):
            errors["username"] = "Username fields must be letter characters only"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password must match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}>".format(self.name)

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = 'Please enter Destination of the trip'
        if len(postData['description']) < 1:
            errors[description] = 'Please enter Description of the trip'
        if (postData['travel_date_from'] < str(datetime.date.today())):
            errors['travel_date_from'] = 'Travel dates should be future-dated'
        if (postData['travel_date_to'] < postData['travel_date_from']):
            errors['travel_date_to'] = "'Travel Date To' should not be before the 'Travel Date From'"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField(auto_now=False, auto_now_add=False)
    travel_date_to = models.DateField(auto_now=False, auto_now_add=False)
    trip_maker = models.ForeignKey(User, related_name="trip_made")
    trip_joiners = models.ManyToManyField(User, related_name="trips_going")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()