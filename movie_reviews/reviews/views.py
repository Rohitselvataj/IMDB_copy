from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import HttpResponse
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
MOVIE_DATA = {
    "The Shawshank Redemption": {
        "_id": "678f678009a7d281db4b59c0",
        "Poster_Link": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNT…",
        "Series_Title": "The Shawshank Redemption",
        "Released_Year": 1994,
        "Certificate": "A",
        "Runtime": "142 min",
        "Genre": "Drama",
        "IMDB_Rating": 9.3,
        "Overview": "Two imprisoned men bond over a number of years, finding solace and eve…",
        "Meta_score": 80,
        "Director": "Frank Darabont",
        "Star1": "Tim Robbins",
        "Star2": "Morgan Freeman",
        "Star3": "Bob Gunton",
        "Star4": "William Sadler",
        "No_of_Votes": 2343110,
        "Gross": "28,341,469"
    },
    "The Godfather": {
        "_id": "678f678009a7d281db4b59c1",
        "Poster_Link": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNW…",
        "Series_Title": "The Godfather",
        "Released_Year": 1972,
        "Certificate": "A",
        "Runtime": "175 min",
        "Genre": "Crime, Drama",
        "IMDB_Rating": 9.2,
        "Overview": "An organized crime dynasty's aging patriarch transfers control of his …",
        "Meta_score": 100,
        "Director": "Francis Ford Coppola",
        "Star1": "Marlon Brando",
        "Star2": "Al Pacino",
        "Star3": "James Caan",
        "Star4": "Diane Keaton",
        "No_of_Votes": 1620367,
        "Gross": "134,966,411"
    }
}

def search_movie(request):
    query = request.GET.get('query')
    movie_details = None

    if query in MOVIE_DATA:
        movie_details = MOVIE_DATA[query]
    else:
        print("No movies found.")

    return render(request, 'search_movie.html', {'movie': movie_details, 'query': query})

def movie_detail(request, movie_id):

    client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/movies?retryWrites=true&w=majority')
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

