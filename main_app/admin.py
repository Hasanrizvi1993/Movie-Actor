# Register your models here.
from django.contrib import admin
from .models import Movie, Actor # import the Cat model from models.py
# Register your models here.

admin.site.register(Movie) # this line will add the model to the admin panel
admin.site.register(Actor) # this line will add the model to the admin panel
