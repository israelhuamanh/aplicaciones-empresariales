from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from .models import Genre, Movie


def recommendations_view(request):
    """
    Vista pública de recomendación — películas del mismo género mejor valoradas —,
    para contrastar qué hace el panel administrativo y qué exige una vista propia.
    """
    genres = Genre.objects.all()
    selected_genre_id = request.GET.get("genre")

    # Películas anotadas con su promedio de valoración y total de votos
    movies_qs = Movie.objects.annotate(
        avg_rating=Avg("ratings__score"),
        rating_count=Count("ratings"),
    ).prefetch_related("genres").select_related("director")

    selected_genre = None
    if selected_genre_id:
        try:
            selected_genre = Genre.objects.get(pk=selected_genre_id)
            # Filtrar películas que pertenecen al género seleccionado
            movies_qs = movies_qs.filter(genres=selected_genre)
        except Genre.DoesNotExist:
            selected_genre = None

    # Ordenar por mejor valoradas (las películas sin valoraciones van al final)
    # y luego por año de estreno más reciente
    recommended_movies = movies_qs.order_by("-avg_rating", "-release_year")

    context = {
        "genres": genres,
        "selected_genre": selected_genre,
        "recommended_movies": recommended_movies,
    }
    return render(request, "movies/recommendations.html", context)


def movie_detail_view(request, pk):
    """
    Vista de detalle para consultar la sinopsis, equipo y valoraciones de una película.
    """
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres", "cast", "ratings").select_related("director"),
        pk=pk,
    )
    context = {
        "movie": movie,
    }
    return render(request, "movies/movie_detail.html", context)
