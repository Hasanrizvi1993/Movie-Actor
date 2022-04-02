from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#actor class model
GENDER_CHOICES = {
    ("f", "female"), 
    ("m", "male")
}
class Actor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES)
    age = models.IntegerField()
    img = models.CharField(max_length=250)
    awards = models.CharField(max_length=200)
    spouse = models.CharField(max_length=200)
    birth_place = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#movie model

class Movie(models.Model):

    title = models.CharField(max_length=50)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ManyToManyField(Actor)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

