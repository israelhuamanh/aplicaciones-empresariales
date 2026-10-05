from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path("", views.recommendations_view, name="recommendations"),
    path("recommendations/", views.recommendations_view, name="recommendations_explicit"),
    path("<int:pk>/", views.movie_detail_view, name="movie_detail"),
]
