from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("categoria/<slug:slug>/", views.category_articles_view, name="category_articles"),
    path("noticia/<slug:slug>/", views.article_detail_view, name="article_detail"),
]
