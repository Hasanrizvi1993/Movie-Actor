from django.shortcuts import render
from django.views.generic.base import TemplateView# <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
from .models import Movie

# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

#about page
class About(TemplateView):
    template_name = "about.html"


#movie
class MovieList(TemplateView):
    template_name = 'movielist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title")
        if title != None:
             # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["movies"] = Movie.objects.filter(name__icontains=title)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {title}"
        else:
            movies = Movie.objects.all()
            context["movies"] = movies # this is where we add the key into our context object for the view to use
            context["header"] = "Our Movies"
        return context

