from django.views.generic import DetailView
from django.shortcuts import render
from django.views.generic.base import TemplateView# <- View class to handle requests
from django.http import HttpResponse, HttpResponseRedirect # <- a class to handle sending a type of response
from .models import Movie, Actor
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views import View # View class to handle requests
from django.urls import reverse
from django.contrib.auth.models import User





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


class Movie_Detail(DetailView):
    model = Movie
    template_name = "movie_detail.html"




class Movie_Create(CreateView):
    model = Movie
    fields = '__all__'
    success_url = '/movies'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/movies')


class Movie_Update(UpdateView):
    model = Movie
    fields = ['title', 'release_year', 'genre', 'img']
    template_name = "movie_update.html"
    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.pk})


class Movie_Delete(DeleteView):
    model = Movie
    template_name = "Movie_delete_confirmation.html"
    success_url = "/movies/"



#ACTOR VIEWS


def actors_index(request):
    actors = Actor.objects.all()
    return render(request, 'actor_index.html', {'actors': actors})

def actors_show(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    return render(request, 'actor_show.html', {'actor': actor})

class ActorCreate(CreateView):
    model = Actor
    fields = '__all__'
    template_name = "actor_form.html"
    success_url = '/actors'

class ActorUpdate(UpdateView):
    model = Actor
    fields = ['name', 'gender', 'age', 'img', 'awards', 'spouse', 'birth_place']
    template_name = "actor_update.html"
    success_url = '/actors'

class ActorDelete(DeleteView):
    model = Actor
    template_name = "actor_confirm_delete.html"
    success_url = '/actors'








def profile(request, username):
    user = User.objects.get(username=username)
    movies = Movie.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'movies': movies})

