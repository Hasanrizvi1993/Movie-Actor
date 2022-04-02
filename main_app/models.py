from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):

    title = models.CharField(max_length=50)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

