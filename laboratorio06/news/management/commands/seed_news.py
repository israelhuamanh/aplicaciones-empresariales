from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Article, Author, Category


class Command(BaseCommand):
    help = "Carga datos iniciales: 3 categorías, autores y al menos 6 noticias realistas."

    def handle(self, *args, **options):
        self.stdout.write("Poblando categorías, autores y noticias para el Laboratorio 6...")

        # 1. Crear al menos 3 Categorías
        cat_tech, _ = Category.objects.get_or_create(
            slug="tecnologia",
            defaults={"name": "Tecnología", "description": "Innovaciones en software, IA y desarrollo de sistemas."},
        )
        cat_biz, _ = Category.objects.get_or_create(
            slug="negocios",
            defaults={"name": "Negocios y Finanzas", "description": "Economía digital, startups y mercados corporativos."},
        )
        cat_inno, _ = Category.objects.get_or_create(
            slug="innovacion",
            defaults={"name": "Innovación y Ciencia", "description": "Avances científicos, robótica y transformación digital."},
        )

        # 2. Crear Autores
        auth_israel, _ = Author.objects.get_or_create(
            name="Israel Angel Huaman",
            defaults={
                "email": "israel.huaman@tecsup.edu.pe",
                "bio": "Desarrollador fullstack y redactor tecnológico especializado en arquitecturas empresariales y Django.",
            },
        )
        auth_lucia, _ = Author.objects.get_or_create(
            name="Lucía Morales",
            defaults={
                "email": "lucia.morales@noticias.com",
                "bio": "Analista de transformación digital y periodista de negocios.",
            },
        )
        auth_carlos, _ = Author.objects.get_or_create(
            name="Carlos Méndez",
            defaults={
                "email": "carlos.mendez@noticias.com",
                "bio": "Investigador en inteligencia artificial y computación en la nube.",
            },
        )

        # 3. Crear 6 Artículos (Noticias) con fechas y categorías
        now = timezone.now()

        articles_data = [
            {
                "title": "Django 6.1 revoluciona el desarrollo de aplicaciones empresariales modernas",
                "slug": "django-6-1-revoluciona-desarrollo-aplicaciones-empresariales",
                "summary": "La nueva versión del framework web para perfeccionistas incluye mejoras determinantes en concurrencia asíncrona, optimizaciones de ORM y un motor de plantillas más ágil.",
                "content": "El ecosistema de Django continúa consolidándose como la plataforma preferida por instituciones y corporaciones para construir plataformas estables y seguras. Con el lanzamiento de Django 6.1, la comunidad ha celebrado la incorporación de directivas avanzadas de renderizado en el motor de plantillas y un rendimiento un 30% superior en las consultas complejas del ORM.\n\nEspecialistas del sector señalan que la facilidad para definir componentes modulares mediante herencia y fragmentos reutilizables agiliza los tiempos de entrega sin comprometer la seguridad frente a vulnerabilidades como Cross-Site Scripting (XSS).",
                "author": auth_israel,
                "categories": [cat_tech, cat_inno],
                "published_date": now - timedelta(hours=2),
            },
            {
                "title": "El auge de la Inteligencia Artificial Generativa en el ecosistema corporativo",
                "slug": "auge-inteligencia-artificial-generativa-ecosistema-corporativo",
                "summary": "Empresas líderes integran agentes autónomos y modelos multimodales para automatizar procesos de ingeniería de software y soporte al cliente.",
                "content": "La transformación digital ha dejado de ser un objetivo a mediano plazo para convertirse en una exigencia operativa cotidiana. Durante el último trimestre, más del 65% de las organizaciones evaluadas reportaron incrementos en su productividad tras desplegar asistentes basados en IA en sus pipelines de desarrollo.\n\nLos analistas destacan que el reto central radica en mantener la gobernanza de datos y la auditabilidad de las operaciones en tiempo real.",
                "author": auth_carlos,
                "categories": [cat_tech],
                "published_date": now - timedelta(days=1, hours=3),
            },
            {
                "title": "Estrategias de inversión en startups tecnológicas de América Latina para 2026",
                "slug": "estrategias-inversion-startups-tecnologicas-latam-2026",
                "summary": "Los fondos de capital de riesgo enfocan su atención en soluciones fintech, cloud computing y seguridad informática con modelos de negocio sostenibles.",
                "content": "El panorama del capital emprendedor en la región experimenta una madurez notable. Los inversores priorizan startups con sólida base tecnológica, margen de rentabilidad claro y arquitectura de software escalable.\n\nPaíses como Perú, Colombia y México encabezan el crecimiento en captación de fondos para proyectos enfocados en digitalización bancaria y servicios empresariales B2B.",
                "author": auth_lucia,
                "categories": [cat_biz],
                "published_date": now - timedelta(days=2),
            },
            {
                "title": "Computación cuántica y ciberseguridad: la nueva frontera de la protección de datos",
                "slug": "computacion-cuantica-ciberseguridad-frontera-proteccion-datos",
                "summary": "Algoritmos post-cuánticos son implementados de forma preventiva para blindar transacciones bancarias ante futuros procesadores de alta potencia.",
                "content": "Científicos e ingenieros de software colaboran en el desarrollo de nuevos protocolos criptográficos inmunes al poder de cálculo cuántico. La encriptación simétrica y asimétrica convencional está siendo reforzada en los centros de datos globales para garantizar la privacidad de los usuarios durante las próximas décadas.",
                "author": auth_carlos,
                "categories": [cat_inno],
                "published_date": now - timedelta(days=3, hours=5),
            },
            {
                "title": "El impacto del teletrabajo híbrido en la eficiencia de los equipos de ingeniería",
                "slug": "impacto-teletrabajo-hibrido-eficiencia-equipos-ingenieria",
                "summary": "Estudios internacionales revelan que la flexibilidad laboral combinada con herramientas colaborativas sincrónicas impulsa la retención del talento clave.",
                "content": "La combinación de oficinas modernas y trabajo remoto ha demostrado ser el esquema de mayor preferencia para desarrolladores y líderes de proyectos. La autonomía en la gestión del tiempo y la claridad en los objetivos por sprints reducen el agotamiento profesional y mejoran la calidad del código entregado.",
                "author": auth_lucia,
                "categories": [cat_biz],
                "published_date": now - timedelta(days=4),
            },
            {
                "title": "Prueba de Escapado Automático en Django: Seguridad activa contra inyección XSS",
                "slug": "prueba-escapado-automatico-django-seguridad-xss",
                "summary": "Demostración del autoescape en el motor de plantillas de Django para mitigar ataques maliciosos de inyección de código HTML.",
                "content": "El motor de plantillas de Django incorpora protección nativa contra inyecciones de código. Como demostración práctica, incluimos texto enriquecido con etiquetas HTML directas: <script>alert('Ataque XSS interceptado con éxito');</script> y <b>Texto en negrita que se muestra como caracteres escapados &lt;b&gt;</b> sin alterar la estructura del documento.",
                "author": auth_israel,
                "categories": [cat_tech, cat_inno],
                "published_date": now - timedelta(days=5),
            },
        ]

        for item in articles_data:
            cats = item.pop("categories")
            article, created = Article.objects.get_or_create(
                slug=item["slug"],
                defaults=item,
            )
            article.categories.set(cats)
            if not created:
                for key, val in item.items():
                    setattr(article, key, val)
                article.save()

        self.stdout.write(self.style.SUCCESS(f"Se crearon y verificaron {len(articles_data)} artículos en 3 categorías."))
