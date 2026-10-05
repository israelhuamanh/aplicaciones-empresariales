from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from news.models import Article, Author, Category


class TemplateEngineTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category_tech = Category.objects.create(
            name="Tecnología",
            slug="tecnologia",
            description="Artículos sobre computación y desarrollo",
        )
        self.category_biz = Category.objects.create(
            name="Negocios",
            slug="negocios",
            description="Artículos empresariales y finanzas",
        )
        self.author = Author.objects.create(
            name="Israel Angel Huaman Huaman",
            email="israel.huaman@tecsup.edu.pe",
            bio="Desarrollador y docente del portal.",
        )
        self.article_1 = Article.objects.create(
            title="Noticia 1: Lanzamiento de Django 6.1",
            slug="noticia-1-lanzamiento-django",
            summary="Resumen de prueba de la noticia tecnológica con palabras clave.",
            content="Cuerpo completo de la noticia sobre desarrollo web y buenas prácticas.",
            author=self.author,
            published_date=timezone.now(),
            is_published=True,
        )
        self.article_1.categories.add(self.category_tech)

        # Artículo para probar escapado automático con HTML y Scripts
        self.article_xss = Article.objects.create(
            title="Noticia de Prueba de Escapado",
            slug="noticia-prueba-escapado",
            summary="Resumen con etiqueta <b>negrita</b> no interpretada.",
            content="Texto con etiquetas <script>alert('xss');</script> y <b>negrita</b>.",
            author=self.author,
            published_date=timezone.now(),
            is_published=True,
        )
        self.article_xss.categories.add(self.category_biz)

    def test_home_view_status_and_templates(self):
        url = reverse("news:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/home.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "news/_article_card.html")
        self.assertContains(response, "Noticia 1: Lanzamiento de Django 6.1")
        self.assertContains(response, "Tecnología")
        self.assertContains(response, "Israel Angel Huaman Huaman")

    def test_category_view_status_and_reusable_fragment(self):
        url = reverse("news:category_articles", kwargs={"slug": self.category_tech.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/category_articles.html")
        self.assertTemplateUsed(response, "news/_article_card.html")
        self.assertContains(response, "Noticia 1: Lanzamiento de Django 6.1")
        self.assertEqual(response.context["category"], self.category_tech)

    def test_article_detail_view(self):
        url = reverse("news:article_detail", kwargs={"slug": self.article_1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/article_detail.html")
        self.assertContains(response, "Noticia 1: Lanzamiento de Django 6.1")
        self.assertContains(response, "Cuerpo completo de la noticia")
        self.assertContains(response, "Israel Angel Huaman Huaman")

    def test_autoescape_protection_xss(self):
        """
        Requisito 12: Comprobar que Django escapa automáticamente el HTML en la plantilla.
        Las etiquetas <script> y <b> deben convertirse en &lt;script&gt; y &lt;b&gt;.
        """
        url = reverse("news:article_detail", kwargs={"slug": self.article_xss.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Debe contener los caracteres HTML escapados
        self.assertContains(response, "&lt;script&gt;alert(&#x27;xss&#x27;);&lt;/script&gt;")
        self.assertContains(response, "&lt;b&gt;negrita&lt;/b&gt;")
        # NO debe contener el script sin escapar ejecutable en el DOM
        self.assertNotContains(response, "<script>alert('xss');</script>")

    def test_empty_state_in_home(self):
        # Despublicar todos los artículos
        Article.objects.all().update(is_published=False)
        url = reverse("news:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay noticias publicadas en este momento.")
