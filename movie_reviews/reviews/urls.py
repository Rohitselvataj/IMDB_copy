from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_movie, name='search_movie'),
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<str:movie_id>/review/', views.add_review, name='add_review'),
    path('test-mongo/', views.test_mongo_connection, name='test_mongo_connection'),
]

