from django.shortcuts import render
from django.views.generic.base import TemplateView# <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response


# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

#about page
class About(TemplateView):
    template_name = "about.html"


#movie
class Movie:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

movies = [
    Movie("Mau", 5, "Female"),
    Movie("Garfield", 43, "Male"),
    Movie("Meowth", 25, "Male"),
    Movie("Salem", 500, "Male"),
]



class MovieList(TemplateView):
    template_name = 'movielist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = movies # this is where we add the key into our context object for the view to use
        return context