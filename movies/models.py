from django.db import models
from django.core import files
import urllib
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import os
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=200)

    def get_movies(self):
        return self.actor_movies.all()

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length= 200)

    def get_movies(self):
        return self.director_movies.all()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def get_movies(self):
        return self.genre_movies.all()

    def __str__(self):
        return self.name


class Movie(models.Model):
    imdb_id = models.CharField(max_length=100, null=True, blank= True)
    title = models.CharField(max_length=100)
    year = models.IntegerField(default=2019,validators = [MaxValueValidator(3000), MinValueValidator(1000)])
    plot = models.TextField()
    language = models.CharField(max_length=100)
    poster = models.ImageField(upload_to = 'movies/', default='', null=True)
    poster_url = models.URLField(null=True, blank=True)
    rating = models.FloatField()
    country = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    actors = models.ManyToManyField(Actor, related_name='actor_movies')
    directors = models.ManyToManyField(Director, related_name='director_movies')

    def get_genre(self):
        return [genre.name for genre in self.genre.all()]

    def get_actors(self):
        return [actor.name for actor in self.actors.all()]

    def get_directors(self):
        return [director.name for director in self.directors.all()]
    
    def set_directors(self, directors):
        try:
            self.directors.set(directors)
        except:
            self.directors.set([directors])
    
    def set_actors(self, actors):
        try:
            self.actors.set(actors)
        except:
            self.actors.set([actors])

    def set_genre(self, genre):
        try:
            self.genre.set(genre)
        except:
            self.genre.set([genre])

    def get_remote_image(self):
        try:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.poster_url).read())
            img_temp.flush()
            self.poster.save(f"image_{self.pk}", File(img_temp))
        except:
            pass

    def get_absolute_url(self):
        return reverse('movies:movie_detail', args=[str(self.id)])

    def __str__(self):
        return self.title