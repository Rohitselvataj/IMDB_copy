from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import HttpResponse

#command
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search_movie')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def search_movie(request):

    client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority')
    db = client['movies']
    movies_collection = db['ratiing']

    movies = []

    query = request.GET.get('query')
    if query:
        print(f"Searching for: {query}")
        movies_cursor = movies_collection.find(
            {"Series_title": {"$regex": query, "$options": "i"}},
            {
                "Series_Title": 1,
                "Genre": 1,
                "Released_Year": 1,
                "Overview": 1,
                "Poster_Link": 1,
                "Certificate": 1,
                "Runtime": 1,
                "IMDB_Rating": 1,
                "Director": 1,
                "Star1": 1,
                "Star2": 1,
                "Star3": 1,
                "Star4": 1,
                "No_of_Votes": 1,
                "Gross": 1
            }
        )
        
        for movie in movies_cursor:
            movie['id'] = str(movie['_id'])  
            movies.append(movie)
            print(f"Found movie: {movie['Series_Title']}")

    client.close()
    
    if not movies:
        print("No movies found.")

    return render(request, 'search_movie.html', {'movies': movies, 'query': query})

def movie_detail(request, movie_id):

    client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority')
    db = client['movies']
    movies_collection = db['ratiing']

    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

    client.close()

    return render(request, 'movie_detail.html', {'movie': movie})

def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(user=request.user, movie=movie, rating=rating, comment=comment)
        return redirect('movie_detail', movie_id=movie.id)
    return render(request, 'add_review.html', {'movie': movie})

def test_mongo_connection(request):
    try:
        # Replace 'mydatabase' with your actual database name
        client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/mydatabase?retryWrites=true&w=majority')
        client.close()
        return HttpResponse("Connected to MongoDB")
    except Exception as e:
        return HttpResponse(f"Error connecting to MongoDB: {e}")

