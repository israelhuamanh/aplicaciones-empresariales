from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Person, Rating


class Command(BaseCommand):
    help = "Crea el superusuario, el grupo editores con sus permisos específicos y un usuario editor de prueba."

    def handle(self, *args, **options):
        # 1. Crear Superusuario si no existe
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = "adminpassword123"

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name="Admin",
                last_name="Principal",
            )
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{admin_username}' creado con éxito."))
        else:
            self.stdout.write(f"Superusuario '{admin_username}' ya existe.")

        # 2. Crear Grupo 'editores'
        # Requisito 9: "Crear un grupo «editores» con permiso para añadir y cambiar películas pero no para eliminarlas"
        group_name = "editores"
        editors_group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Grupo '{group_name}' creado."))
        else:
            self.stdout.write(f"Grupo '{group_name}' ya existía.")

        # Configurar permisos para 'Movie'
        movie_ct = ContentType.objects.get_for_model(Movie)
        add_movie_perm = Permission.objects.get(content_type=movie_ct, codename="add_movie")
        change_movie_perm = Permission.objects.get(content_type=movie_ct, codename="change_movie")
        view_movie_perm = Permission.objects.get(content_type=movie_ct, codename="view_movie")
        delete_movie_perm = Permission.objects.get(content_type=movie_ct, codename="delete_movie")

        # Permisos adicionales para que los editores puedan ver géneros y personas al editar películas
        genre_ct = ContentType.objects.get_for_model(Genre)
        view_genre_perm = Permission.objects.get(content_type=genre_ct, codename="view_genre")

        person_ct = ContentType.objects.get_for_model(Person)
        view_person_perm = Permission.objects.get(content_type=person_ct, codename="view_person")

        rating_ct = ContentType.objects.get_for_model(Rating)
        view_rating_perm = Permission.objects.get(content_type=rating_ct, codename="view_rating")
        add_rating_perm = Permission.objects.get(content_type=rating_ct, codename="add_rating")
        change_rating_perm = Permission.objects.get(content_type=rating_ct, codename="change_rating")

        # Asignar permisos estrictos: add, change, view en Movie (SIN delete)
        permissions_to_set = [
            add_movie_perm,
            change_movie_perm,
            view_movie_perm,
            view_genre_perm,
            view_person_perm,
            view_rating_perm,
            add_rating_perm,
            change_rating_perm,
        ]
        editors_group.permissions.set(permissions_to_set)
        # Garantizar que delete_movie NO esté en el grupo
        editors_group.permissions.remove(delete_movie_perm)
        self.stdout.write(self.style.SUCCESS(f"Permisos asignados al grupo '{group_name}' (sin permiso de eliminación)."))

        # 3. Crear usuario editor de prueba
        editor_username = "editor1"
        editor_password = "editorpassword123"

        if not User.objects.filter(username=editor_username).exists():
            editor_user = User.objects.create_user(
                username=editor_username,
                email="editor1@example.com",
                password=editor_password,
                first_name="Carlos",
                last_name="Editor",
                is_staff=True,  # Necesario para ingresar al panel /admin/
            )
            editor_user.groups.add(editors_group)
            self.stdout.write(self.style.SUCCESS(f"Usuario editor '{editor_username}' creado con acceso al panel."))
        else:
            editor_user = User.objects.get(username=editor_username)
            editor_user.is_staff = True
            editor_user.save()
            editor_user.groups.add(editors_group)
            self.stdout.write(f"Usuario editor '{editor_username}' ya existe y fue sincronizado.")
