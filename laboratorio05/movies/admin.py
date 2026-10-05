from django.contrib import admin
from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """
    Permite registrar y editar valoraciones directamente dentro del
    formulario de la película sin salir del registro padre.
    """
    model = Rating
    extra = 1
    fields = ("author", "score", "comment", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_year",
        "duration_minutes",
        "director",
        "display_genres",
        "display_average_rating",
        "created_at",
    )
    list_filter = ("genres", "release_year")
    search_fields = ("title", "director__first_name", "director__last_name")
    ordering = ("-release_year", "title")
    filter_horizontal = ("genres", "cast")
    readonly_fields = ("created_at", "updated_at")
    inlines = [RatingInline]

    fieldsets = (
        (
            "Información Principal",
            {
                "fields": (
                    "title",
                    "original_title",
                    "synopsis",
                    "release_year",
                    "duration_minutes",
                    "poster",
                )
            },
        ),
        (
            "Equipo y Categorización",
            {
                "fields": ("director", "genres", "cast"),
            },
        ),
        (
            "Auditoría",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    @admin.display(description="Géneros")
    def display_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])

    @admin.display(description="Valoración Promedio")
    def display_average_rating(self, obj):
        avg = obj.average_rating
        return f"{avg}/10" if avg is not None else "Sin valoraciones"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "primary_role", "birth_date", "created_at")
    list_filter = ("primary_role",)
    search_fields = ("first_name", "last_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "score", "author", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("movie__title", "author", "comment")
    readonly_fields = ("created_at", "updated_at")
