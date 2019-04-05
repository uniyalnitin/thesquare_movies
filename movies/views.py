import requests
from django.core import files
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from .models import Movie, Genre, Director, Actor
from .forms import MovieForm, ApiForm
from .utils import *
import json
# Create your views here.

APIKEY = "e608cffb"

def index(request):
    movies = Movie.objects.all()[:10]

    return render(request, 'index.html')


def actor_list(request):
    page = request.GET.get('page', 1) 
    page_size = request.GET.get('page_size', 10) 

    actor_list = Actor.objects.all()

    search_param = request.GET.get('search',None)

    if search_param:
        actor_list = actor_list.filter(name__icontains=search_param)
    
    paginator = Paginator(actor_list, page_size)

    try:
        actors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actors = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        actors = paginator.page(paginator.num_pages)

    actors = paginator.get_page(page)

    return render(request, 'list.html', {'actors':actors, 'data':actors,'page':page, 'page_size':page_size})

def director_list(request):
    page = request.GET.get('page', 1) 
    page_size = request.GET.get('page_size', 10) 

    director_list = Director.objects.all()

    search_param = request.GET.get('search',None)

    if search_param:
        director_list = director_list.filter(name__icontains=search_param)
    
    paginator = Paginator(director_list, page_size)

    try:
        directors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        directors = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        directors = paginator.page(paginator.num_pages)

    directors = paginator.get_page(page)

    return render(request, 'list.html', {'directors':directors, 'data':directors,'page':page, 'page_size':page_size})


def movie_list(request):
    page = request.GET.get('page', 1) 
    page_size = request.GET.get('page_size', 10) # default 10 movies per page if page_size is not in query string

    search_param = request.GET.get('search', None)
    genre_param = request.GET.get('genre', None)
    actor_param = request.GET.get('actors', None)
    director_param = request.GET.get('directors', None)

    movie_list = Movie.objects.all()

    if search_param:
        movie_list = movie_list.filter(title__icontains=search_param)

    if genre_param:
        genre = get_object_or_404(Genre,name = genre_param)
        movie_list = movie_list.filter(genre__in = [genre])
    
    if actor_param:
        actor = get_object_or_404(Actor, name = actor_param)
        movie_list = movie_list.filter(actors__in = [actor])
    if director_param:
        director = get_object_or_404(Director, name = director_param)
        movie_list = movie_list.filter(directors__in = [director])

    paginator = Paginator(movie_list, page_size)

    # try:
    #     movies = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer deliver the first page
    #     movies = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range deliver last page of results
        # movies = paginator.page(paginator.num_pages)

    movies = paginator.get_page(page)

    return render(request, 'movie/movie_list.html', {'movies': movies, 'page':page, 'page_size':page_size, 'genre_filter': genre_param, 'actor_filter': actor_param, 'director_filter': director_param})
    
def movie_detail(request, id):
    movie = Movie.objects.get(id=id)

    return render(request, 'movie/movie_detail.html', {'movie': movie})

def full_search(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    options = request.GET.get('options', 'movies')
    search = request.GET.get('search', '')

    movies= None
    actors = None
    directors = None 
    genre = None
    if options=='movies':
        movie_list = Movie.objects.filter(title__icontains=search)
        paginator = Paginator(movie_list, page_size)
        movies = paginator.get_page(page)

    elif options=='actors':
        actor_list = Actor.objects.filter(name__icontains=search)
        paginator = Paginator(actor_list, page_size)
        actors = paginator.get_page(page)

    elif options == 'directors':
        director_list = Director.objects.filter(name__icontains=search)
        paginator = Paginator(director_list, page_size)
        directors = paginator.get_page(page)

    elif options == 'genre':
        genre_list = Genre.objects.filter(name__icontains=search)
        paginator = Paginator(genre_list, page_size)
        genre = paginator.get_page(page)

    return render(request, 'list.html', {'movies': movies, 'actors':actors, 'directors':directors, 'genre': genre, 'page':page, 'page_size':page_size})

def movie_create(request):

    if request.POST:
        form = MovieForm(request.POST)

        if form.is_valid():
            movie = form.save()
            
            return redirect(reverse('movies:movie_list'))
    else:
        form = MovieForm()
    messages.success(request, 'Data successfully saved.')
    return render(request, 'movie/form.html', {'form': form})

def movie_update(request, id):
    object = Movie.objects.get(id=id)
    if request.POST:
        form = MovieForm(request.POST, instance=object)

        if form.is_valid():
            form.save()
            messages.success(request, 'Movie details updated.')
            # object.save()
        else:
            messages.error(request, 'Error, Movie Details cannot be modified.')
    else:
        form = MovieForm(instance=object)
    
    return render(request, 'movie/form.html', {'form':form, 'edit':True})

def movie_delete(request, id):
    Movie.objects.get(id=id).delete()
    messages.success(request, 'Movie delete successfully')
    return redirect(reverse('movies:movie_list'))

def api_fetch_movie(request):
    api = API(request, APIKEY)
    error = None
    saved = False
    if request.POST:
        form = ApiForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title', None)
            imdb_id = form.cleaned_data.get('imdb_id', None)
            key_word = form.cleaned_data.get('key_word', None)

            if imdb_id:
                json_response = api.fetch_by_id(imdb_id)
            elif title:
                json_response= api.fetch_by_tite(title)
            # data = json.loads(json_response)
            movie = json_response.json()

            opn = response_handler(request, movie)
            if opn:
                return redirect(reverse('movies:movie_list'))
    else:
        form = ApiForm()
    return render(request, 'movie/form.html', {'form':form, 'saved':saved, 'error':error})