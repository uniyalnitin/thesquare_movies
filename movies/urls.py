from django.urls import path
from .views import *

app_name = "movies"

urlpatterns = [
    path('', index, name='index'),
    path('movies/', movie_list, name="movie_list"),
    path('movies/<int:id>/', movie_detail, name="movie_detail"),
    path("search/", full_search, name="full_search"),
    path('movies/new/', movie_create, name="movie_create"),
    path("movies/edit/<int:id>/", movie_update, name="movie_edit"),
    path("movies/delete/<int:id>/", movie_delete, name="movie_delete"),
    path("actors/", actor_list, name="actor_list"),
    path("directors/", director_list, name="director_list"),
    path("api/fetch_movie/", api_fetch_movie, name="fetch_movie"),
    path("api/fetch_movie/<add>/", api_fetch_movie, name="add_movie"),
]