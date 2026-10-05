from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Article, Category


def home_view(request):
    """
    Portada del portal de noticias.
    Recorre las noticias publicadas con fecha decreciente.
    """
    articles_list = (
        Article.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related("categories")
        .order_by("-published_date")
    )
    recent_articles = articles_list[:5]

    context = {
        "articles": articles_list,
        "recent_articles": recent_articles,
    }
    return render(request, "news/home.html", context)


def category_articles_view(request, slug):
    """
    Listado de noticias pertenecientes a una categoría específica.
    Reutiliza el fragmento de tarjeta _article_card.html.
    """
    category = get_object_or_404(Category, slug=slug)
    articles_list = (
        category.articles.filter(is_published=True)
        .select_related("author")
        .prefetch_related("categories")
        .order_by("-published_date")
    )
    recent_articles = (
        Article.objects.filter(is_published=True)
        .order_by("-published_date")[:5]
    )

    context = {
        "category": category,
        "articles": articles_list,
        "recent_articles": recent_articles,
    }
    return render(request, "news/category_articles.html", context)


def article_detail_view(request, slug):
    """
    Ficha de detalle de la noticia.
    Muestra la noticia completa, autor, fecha, categorías e imagen.
    """
    article = get_object_or_404(
        Article.objects.select_related("author").prefetch_related("categories"),
        slug=slug,
        is_published=True,
    )
    recent_articles = (
        Article.objects.filter(is_published=True)
        .exclude(id=article.id)
        .order_by("-published_date")[:5]
    )

    context = {
        "article": article,
        "recent_articles": recent_articles,
    }
    return render(request, "news/article_detail.html", context)
