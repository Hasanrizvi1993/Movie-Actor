from dataclasses import field, fields
from re import template
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView# <- View class to handle requests
from django.http import HttpResponse, HttpResponseRedirect # <- a class to handle sending a type of response
from .models import Movie, Actor, Review
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views import View # View class to handle requests
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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
#addtion to movie_detail for like functionality
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Movie, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context

@method_decorator(login_required, name='dispatch')
class Movie_Create(CreateView):
    model = Movie
    fields = ['title', 'release_year', 'genre', 'img', 'actors']
    template_name= "movie_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/movies')

@method_decorator(login_required, name='dispatch')
class Movie_Update(UpdateView):
    model = Movie
    fields = ['title', 'release_year', 'genre', 'img', 'actors']
    template_name = "movie_update.html"
    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class Movie_Delete(DeleteView):
    model = Movie
    template_name = "Movie_delete_confirmation.html"
    success_url = "/movies/"

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    movies = Movie.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'movies': movies})

#ACTOR VIEWS
def actor_home(request):
    actors = Actor.objects.all()
    return render(request, 'actor_index.html', {'actors': actors})

def actors_show(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    return render(request, 'actor_show.html', {'actor': actor})

@method_decorator(login_required, name='dispatch')
class ActorCreate(CreateView):
    model = Actor
    fields = '__all__'
    template_name = "actor_form.html"
    success_url = '/actors'

@method_decorator(login_required, name='dispatch')
class ActorUpdate(UpdateView):
    model = Actor
    fields = ['name', 'gender', 'age', 'img', 'awards', 'spouse', 'birth_place']
    template_name = "actors_update.html"
    success_url = '/actors'

@method_decorator(login_required, name='dispatch')
class ActorDelete(DeleteView):
    model = Actor
    template_name = "actor_confirm_delete.html"
    success_url = '/actors'

#review views
class AddReviewView(CreateView):
    model = Review
    template_name = "add_review.html"
    fields = '__all__'
    success_url = '/movies/'

# django auth
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('HEY', user.username)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/movies')

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else: # it was a get request so send the emtpy login form
        # form = LoginForm()
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

#like views
def LikeView(request, pk):
    movie = get_object_or_404(Movie, id=request.POST.get('movie_id'))
    movie.likes.add(request.user)
    return HttpResponseRedirect(reverse('movie_detail', args=[str(pk)]))