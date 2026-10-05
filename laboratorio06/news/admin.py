from django.contrib import admin
from .models import Article, Author, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "is_published", "display_categories")
    list_filter = ("is_published", "categories", "published_date")
    search_fields = ("title", "summary", "content", "author__name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Información Principal",
            {
                "fields": ("title", "slug", "author", "categories", "is_published"),
            },
        ),
        (
            "Contenido y Multimedia",
            {
                "fields": ("summary", "content", "featured_image"),
            },
        ),
        (
            "Fechas y Auditoría",
            {
                "classes": ("collapse",),
                "fields": ("published_date", "created_at", "updated_at"),
            },
        ),
    )

    @admin.display(description="Categorías")
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
