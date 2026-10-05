from datetime import date
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse
from movies.models import Genre, Movie, Person, Rating


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.genre_action = Genre.objects.create(name="Acción", description="Películas de acción")
        self.genre_sci_fi = Genre.objects.create(name="Ciencia Ficción", description="Películas futuristas")

        self.director = Person.objects.create(
            first_name="Christopher",
            last_name="Nolan",
            birth_date=date(1970, 7, 30),
            primary_role=Person.RoleChoices.DIRECTOR,
        )
        self.actor = Person.objects.create(
            first_name="Leonardo",
            last_name="DiCaprio",
            birth_date=date(1974, 11, 11),
            primary_role=Person.RoleChoices.ACTOR,
        )

        self.movie = Movie.objects.create(
            title="Inception",
            original_title="Inception",
            synopsis="Mundo de los sueños",
            release_year=2010,
            duration_minutes=148,
            director=self.director,
        )
        self.movie.genres.add(self.genre_action, self.genre_sci_fi)
        self.movie.cast.add(self.actor)

        self.rating1 = Rating.objects.create(
            movie=self.movie,
            author="Crítico 1",
            score=9,
            comment="Excelente",
        )
        self.rating2 = Rating.objects.create(
            movie=self.movie,
            author="Crítico 2",
            score=7,
            comment="Buena",
        )

    def test_model_str_representations(self):
        self.assertEqual(str(self.genre_action), "Acción")
        self.assertEqual(str(self.director), "Christopher Nolan")
        self.assertEqual(str(self.movie), "Inception (2010)")
        self.assertIn("Inception - 9/10", str(self.rating1))

    def test_movie_relationships_and_aggregations(self):
        self.assertEqual(self.movie.genres.count(), 2)
        self.assertEqual(self.movie.cast.count(), 1)
        self.assertEqual(self.movie.director.last_name, "Nolan")
        self.assertEqual(self.movie.total_ratings, 2)
        # Promedio de 9 y 7 es 8.0
        self.assertEqual(self.movie.average_rating, 8.0)

    def test_audit_timestamps(self):
        self.assertIsNotNone(self.movie.created_at)
        self.assertIsNotNone(self.movie.updated_at)
        self.assertIsNotNone(self.genre_action.created_at)
        self.assertIsNotNone(self.director.created_at)
        self.assertIsNotNone(self.rating1.created_at)


class RecommendationsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre_drama = Genre.objects.create(name="Drama")
        self.genre_scifi = Genre.objects.create(name="Sci-Fi")

        # Película A con promedio 9
        self.movie_a = Movie.objects.create(
            title="Película A",
            synopsis="Sinopsis A",
            release_year=2020,
        )
        self.movie_a.genres.add(self.genre_drama)
        Rating.objects.create(movie=self.movie_a, author="A1", score=9)

        # Película B con promedio 7
        self.movie_b = Movie.objects.create(
            title="Película B",
            synopsis="Sinopsis B",
            release_year=2021,
        )
        self.movie_b.genres.add(self.genre_drama)
        Rating.objects.create(movie=self.movie_b, author="B1", score=7)

        # Película C de otro género
        self.movie_c = Movie.objects.create(
            title="Película C",
            synopsis="Sinopsis C",
            release_year=2022,
        )
        self.movie_c.genres.add(self.genre_scifi)
        Rating.objects.create(movie=self.movie_c, author="C1", score=10)

    def test_recommendations_page_status_and_template(self):
        url = reverse("movies:recommendations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/recommendations.html")
        self.assertContains(response, "Película A")
        self.assertContains(response, "Película B")
        self.assertContains(response, "Película C")

    def test_recommendations_genre_filtering(self):
        url = reverse("movies:recommendations")
        response = self.client.get(url, {"genre": self.genre_drama.id})
        self.assertEqual(response.status_code, 200)
        # Solo deben salir las del género drama
        movies_in_context = list(response.context["recommended_movies"])
        self.assertIn(self.movie_a, movies_in_context)
        self.assertIn(self.movie_b, movies_in_context)
        self.assertNotIn(self.movie_c, movies_in_context)
        # Comprobar que la de mayor puntuación (9) aparece primero que la de menor (7)
        self.assertEqual(movies_in_context[0], self.movie_a)
        self.assertEqual(movies_in_context[1], self.movie_b)

    def test_movie_detail_view(self):
        url = reverse("movies:movie_detail", kwargs={"pk": self.movie_a.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/movie_detail.html")
        self.assertContains(response, "Película A")
        self.assertContains(response, "Sinopsis A")


class PermissionsAndRolesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admin_test",
            email="admin@test.com",
            password="testpassword123",
        )

        # Crear grupo editores con permisos de add y change, pero NO delete
        self.group = Group.objects.create(name="editores")
        movie_ct = ContentType.objects.get_for_model(Movie)
        add_perm = Permission.objects.get(content_type=movie_ct, codename="add_movie")
        change_perm = Permission.objects.get(content_type=movie_ct, codename="change_movie")
        view_perm = Permission.objects.get(content_type=movie_ct, codename="view_movie")
        self.group.permissions.add(add_perm, change_perm, view_perm)

        # Usuario editor dentro del grupo
        self.editor_user = User.objects.create_user(
            username="editor_test",
            password="testpassword123",
            is_staff=True,
        )
        self.editor_user.groups.add(self.group)

        # Usuario normal sin staff ni permisos
        self.normal_user = User.objects.create_user(
            username="normal_test",
            password="testpassword123",
            is_staff=False,
        )

        self.movie = Movie.objects.create(
            title="Película Prueba",
            synopsis="Sinopsis",
            release_year=2023,
        )

    def test_group_has_add_and_change_but_not_delete(self):
        self.assertTrue(self.editor_user.has_perm("movies.add_movie"))
        self.assertTrue(self.editor_user.has_perm("movies.change_movie"))
        self.assertTrue(self.editor_user.has_perm("movies.view_movie"))
        # Estrictamente no debe tener delete_movie
        self.assertFalse(self.editor_user.has_perm("movies.delete_movie"))

    def test_editor_cannot_delete_in_admin(self):
        # Iniciar sesión como editor
        self.client.login(username="editor_test", password="testpassword123")
        delete_url = reverse("admin:movies_movie_delete", args=[self.movie.pk])
        response = self.client.get(delete_url)
        # Debe recibir 403 Forbidden porque no tiene permiso delete_movie
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_delete_in_admin(self):
        # Iniciar sesión como superusuario
        self.client.login(username="admin_test", password="testpassword123")
        delete_url = reverse("admin:movies_movie_delete", args=[self.movie.pk])
        response = self.client.get(delete_url)
        # Superuser sí tiene permiso para acceder a la confirmación de borrado
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_access_admin(self):
        self.client.login(username="normal_test", password="testpassword123")
        admin_url = reverse("admin:index")
        response = self.client.get(admin_url)
        # Redirige al login de admin porque is_staff=False
        self.assertEqual(response.status_code, 302)
