from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Person(models.Model):
    class RoleChoices(models.TextChoices):
        ACTOR = "ACTOR", "Actor / Actriz"
        DIRECTOR = "DIRECTOR", "Director(a)"
        PRODUCER = "PRODUCER", "Productor(a)"
        WRITER = "WRITER", "Guionista"

    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    biography = models.TextField(blank=True, verbose_name="Biografía")
    primary_role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.ACTOR,
        verbose_name="Rol principal",
    )
    photo = models.ImageField(upload_to="people/", blank=True, null=True, verbose_name="Fotografía")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    original_title = models.CharField(max_length=200, blank=True, verbose_name="Título original")
    synopsis = models.TextField(verbose_name="Sinopsis")
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1888), MaxValueValidator(2100)],
        verbose_name="Año de estreno",
    )
    duration_minutes = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Duración (minutos)",
    )
    poster = models.ImageField(upload_to="posters/", blank=True, null=True, verbose_name="Póster")
    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
        verbose_name="Géneros",
    )
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directed_movies",
        verbose_name="Director(a)",
    )
    cast = models.ManyToManyField(
        Person,
        blank=True,
        related_name="acted_movies",
        verbose_name="Reparto / Actores",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ["-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    @property
    def average_rating(self):
        avg = self.ratings.aggregate(models.Avg("score"))["score__avg"]
        return round(avg, 2) if avg is not None else None

    @property
    def total_ratings(self):
        return self.ratings.count()


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Película",
    )
    author = models.CharField(max_length=100, default="Anónimo", verbose_name="Autor / Crítico")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Puntuación (1-10)",
        help_text="Valor numérico entre 1 y 10",
    )
    comment = models.TextField(blank=True, verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.movie.title} - {self.score}/10 ({self.author})"
