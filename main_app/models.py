from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

#actor class model
GENDER_CHOICES = {
    ("F", "female"), 
    ("M", "male")
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
    actors = models.ManyToManyField(Actor)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

#review model
class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    review_content = models.CharField(max_length=100)
    rating = models.FloatField(
    validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )       

    def __str__(self):
        return '%s - %s' % (self.movie, self.review_content) 
