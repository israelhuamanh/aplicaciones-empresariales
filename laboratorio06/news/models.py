from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Identificador (slug)")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre completo")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")
    bio = models.TextField(blank=True, verbose_name="Biografía")
    avatar = models.ImageField(upload_to="authors/", blank=True, null=True, verbose_name="Foto / Avatar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="Título")
    slug = models.SlugField(max_length=260, unique=True, verbose_name="Identificador (slug)")
    summary = models.TextField(verbose_name="Resumen / Copete", help_text="Breve descripción para listados y tarjetas.")
    content = models.TextField(verbose_name="Cuerpo de la noticia", help_text="Contenido completo.")
    featured_image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True,
        verbose_name="Imagen destacada",
    )
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de publicación")
    is_published = models.BooleanField(default=True, verbose_name="¿Publicado?")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Autor",
    )
    categories = models.ManyToManyField(
        Category,
        related_name="articles",
        verbose_name="Categorías",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Noticia / Artículo"
        verbose_name_plural = "Noticias / Artículos"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
