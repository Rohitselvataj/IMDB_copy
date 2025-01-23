from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import HttpResponse
from .forms import MovieForm, ReviewForm
from django.contrib.auth.decorators import login_required

MONGODB_URI = 'mongodb://localhost:27017/'
#command
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user =form.get_user()
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
    review_collection = db['stars']
    
    if query:
        # Search for movies in the MongoDB collection
        movie_details = movies_collection.find_one({"Series_Title": query})
    else:
        print("No movies found.")

    
    if movie_details:
        movie_details['_id'] = str(movie_details['_id'])
        
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            review_data = {
                "series_title": movie_details['Series_Title'],
                "user": request.user.username,
                "rating": rating,
                "comment": comment,
            }
                    # Insert review into MongoDB
            review_collection.insert_one(review_data)
            return redirect('search_movie')
        
    
    client.close()

    return render(request, 'search_movie.html', {'movie': movie_details, 'query': query})


@login_required  # Ensure the user is logged in
def add_review(request, movie_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['movies']
    review_collection = db['stars']  # Assuming 'stars' is your collection for reviews

    # Fetch the movie by its ObjectId
    movie = db['ratiing'].find_one({"_id": ObjectId(movie_id)})

    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        
        # Prepare review data
        review_data = {
            "series_title": movie['Series_Title'],  # Use Series_Title to associate the review
            "user": request.user.username,  # Store the username
            "rating": rating,
            "comment": comment,
        }
        
        # Insert review into MongoDB
        review_collection.insert_one(review_data)
        return redirect('movie_detail', movie_id=movie_id)  # Redirect to the movie detail page
    else:
        # If GET request, create an empty form
        form = ReviewForm()

    client.close()
    
    return render(request, 'add_review.html', {'movie': movie})


def test_mongo_connection(request):
    try:
        # Replace 'mydatabase' with your actual database name
        client = MongoClient('mongodb://localhost:27017/')
        client.close()
        return HttpResponse("Connected to MongoDB")
    except Exception as e:
        return HttpResponse(f"Error connecting to MongoDB: {e}")

