from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import HttpResponse
from .forms import MovieForm
MONGODB_URI = 'mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority'
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
    query = request.GET.get('query')
    movie_details = None
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['movies']
    movies_collection = db['ratiing']
    
    if query:
        # Search for movies in the MongoDB collection
        movie_details = movies_collection.find_one({"Series_Title": query})
    else:
        print("No movies found.")
    client.close()

    return render(request, 'search_movie.html', {'movie': movie_details, 'query': query})

def movie_detail(request, movie_id):

    client = MongoClient('mongodb://localhost:27017/')
    db = client['movies']
    movies_collection = db['ratiing']

    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

    client.close()
    
    if movie is None:
        return HttpResponse("Movie not found", status=404)

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
        client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority')
        client.close()
        return HttpResponse("Connected to MongoDB")
    except Exception as e:
        return HttpResponse(f"Error connecting to MongoDB: {e}")

