from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_movie, name='search_movie'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
]

