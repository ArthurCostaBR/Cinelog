from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('search/', views.search_view, name="search"),
    path('<str:media_type>/<int:tmdb_id>/', views.details_view, name="details"),
]