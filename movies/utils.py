import requests
from django.contrib import messages
from .models import Actor, Director, Genre, Movie

class API:

    def __init__(self, request, apikey):
        self.request = request
        self.url = "http://www.omdbapi.com/"
        self.end_string = "&type=movie&r=json&apikey={}".format(apikey)

    def fetch_by_id(self, id, year=None):
        query_string= '?i={}'.format(id)
        if year:
            query_string += "&y={}".format(year)
        response = self.request.get(self.url + query_string + self.end_string)
        return response
    
    def fetch_by_tite(self, title, year=None):
        query_string = '?t={}'.format(title)
        if year:
            query_string += "&y={}".format(year)
        url = self.url + query_string + self.end_string
        print(url)
        response = requests.get(url)
        return response
    
    def fetch_by_search_param(self, search, year=None):
        query_string = '?s={}'.format(search)
        if year:
            query_string += "&y={}".format(year)
        response = self.request.get(self.url + query_string + self.end_string)
        return response


def response_handler(request, movie):
    if movie["Response"]=="True":
        title = movie["Title"]
        imdb_id = movie["imdbID"]
        year = movie["Year"]
        plot = movie["Plot"]
        language = movie["Language"]
        poster_url = movie["Poster"]
        rating = movie["imdbRating"]
        country = movie["Country"]
        genre_list = [genre.strip() for genre in movie["Genre"].split(",")]
        actor_list = [actor.strip() for actor in movie["Actors"].split(",")]
        director_list = [director.strip() for director in movie["Director"].split(",")]

        genre = []
        actors = []
        directors =[]
        for item in genre_list:
            try:
                obj = Genre.objects.get(name__iexact=item)
                genre.append(obj)
            except Genre.DoesNotExist:
                obj = Genre.objects.create(name=item)
                genre.append(obj)
            except:
                pass
        for item in actor_list:
            try:
                obj = Actor.objects.get(name__iexact=item)
                actors.append(obj)
            except Actor.DoesNotExist:
                obj = Actor.objects.create(name=item)
                actors.append(obj)
            except:
                pass
        for item in director_list:
            try:
                obj = Director.objects.get(name__iexact=item)
                directors.append(obj)
            except Director.DoesNotExist:
                obj = Director.objects.create(name=item)
                directors.append(obj)
            except:
                pass
        
        try:
            obj = Movie.objects.get(title=title)
            obj.imdb_id = imdb_id
            obj.year = year
            obj.plot = plot
            obj.language = language
            obj.poster_url = poster_url
            obj.rating = rating
            obj.country = country
            obj.set_genre(genre)
            obj.set_actors(actors)
            obj.set_directors(directors)
            obj.get_remote_image()
            obj.save()
            saved = True
        except Movie.DoesNotExist:
            obj = Movie.objects.create(imdb_id=imdb_id, title=title, year=year, plot=plot, language=language, poster_url=poster_url, rating=rating, country=country)
            obj.set_genre(genre)
            obj.set_actors(actors)
            obj.set_directors(directors)
            obj.get_remote_image()
            obj.save()
            saved = True
        except:
            saved = False
            messages.error(request, 'Error, Data is not saved!.')
            return False   
        messages.success(request, 'Data Successfully Saved.')

        return True
    elif movie["Response"]=='False':
        messages.error(request, 'Movie Not Found')
    else:
        messages.error(request, 'Cannot connect with the server')
    return False 