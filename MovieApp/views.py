from django.shortcuts import render, redirect, get_object_or_404
from .forms import MovieForm
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "MovieApp/movie_list.html", {"movies": movies})

def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("movies:add")
    else:
        form = MovieForm()

    return render(request, "MovieApp/movie_form.html", {"form":form})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, "MovieApp/movie_detail.html", {"movie":movie})