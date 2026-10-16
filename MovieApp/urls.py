from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path("", views.movie_list, name="index"),
    path("add/", views.movie_create, name="add"),
    path("movies/<int:pk>/", views.movie_detail, name="detail"),
]