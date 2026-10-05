from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el superusuario del portal de noticias para el Laboratorio 6."

    def handle(self, *args, **options):
        admin_username = "admin"
        admin_email = "admin@noticiasempresariales.com"
        admin_password = "adminpassword123"

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name="Administrador",
                last_name="Portal",
            )
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{admin_username}' creado exitosamente."))
        else:
            self.stdout.write(f"Superusuario '{admin_username}' ya existe.")
