from datetime import date
from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Person, Rating


class Command(BaseCommand):
    help = "Carga datos iniciales realistas: 4+ géneros, personas (directores y actores), 10 películas y valoraciones."

    def handle(self, *args, **options):
        self.stdout.write("Iniciando carga de datos...")

        # 1. Crear Géneros (al menos 4)
        genres_data = [
            {"name": "Ciencia Ficción", "description": "Películas especulativas sobre ciencia, futuro y tecnología."},
            {"name": "Drama", "description": "Obras con enfoque en conflictos emocionales y desarrollo de personajes."},
            {"name": "Acción", "description": "Películas con secuencias de alto impacto, persecuciones y combates."},
            {"name": "Crimen / Suspenso", "description": "Narrativas sobre crímenes, misterios y tensiones psicológicas."},
            {"name": "Animación", "description": "Producciones animadas de alta calidad técnica y narrativa."},
        ]

        genre_objs = {}
        for g in genres_data:
            obj, _ = Genre.objects.get_or_create(name=g["name"], defaults={"description": g["description"]})
            genre_objs[g["name"]] = obj
        self.stdout.write(self.style.SUCCESS(f"Géneros verificados: {len(genre_objs)}"))

        # 2. Crear Personas (Directores y Actores)
        people_data = [
            {
                "first_name": "Christopher",
                "last_name": "Nolan",
                "birth_date": date(1970, 7, 30),
                "primary_role": Person.RoleChoices.DIRECTOR,
                "biography": "Reconocido director británico-estadounidense célebre por narrativas complejas y visuales imponentes.",
            },
            {
                "first_name": "Denis",
                "last_name": "Villeneuve",
                "birth_date": date(1967, 10, 3),
                "primary_role": Person.RoleChoices.DIRECTOR,
                "biography": "Director y guionista canadiense aclamado por sus películas de ciencia ficción y atmósferas envolventes.",
            },
            {
                "first_name": "Martin",
                "last_name": "Scorsese",
                "birth_date": date(1942, 11, 17),
                "primary_role": Person.RoleChoices.DIRECTOR,
                "biography": "Uno de los directores más influyentes en la historia del cine moderno, especialista en drama y crimen.",
            },
            {
                "first_name": "Quentin",
                "last_name": "Tarantino",
                "birth_date": date(1963, 3, 27),
                "primary_role": Person.RoleChoices.DIRECTOR,
                "biography": "Director conocido por sus diálogos mordaces, estructuras no lineales y homenajes al cine de género.",
            },
            {
                "first_name": "Hayao",
                "last_name": "Miyazaki",
                "birth_date": date(1941, 1, 5),
                "primary_role": Person.RoleChoices.DIRECTOR,
                "biography": "Legendario maestro del anime y cofundador de Studio Ghibli.",
            },
            {
                "first_name": "Leonardo",
                "last_name": "DiCaprio",
                "birth_date": date(1974, 11, 11),
                "primary_role": Person.RoleChoices.ACTOR,
                "biography": "Actor estadounidense ganador del Oscar con una vasta carrera en cine dramático.",
            },
            {
                "first_name": "Christian",
                "last_name": "Bale",
                "birth_date": date(1974, 1, 30),
                "primary_role": Person.RoleChoices.ACTOR,
                "biography": "Actor británico conocido por su extraordinaria versatilidad y transformaciones físicas.",
            },
            {
                "first_name": "Timothée",
                "last_name": "Chalamet",
                "birth_date": date(1995, 12, 27),
                "primary_role": Person.RoleChoices.ACTOR,
                "biography": "Joven actor nominado al Oscar, protagonista de grandes epopeyas contemporáneas.",
            },
            {
                "first_name": "Robert",
                "last_name": "De Niro",
                "birth_date": date(1943, 8, 17),
                "primary_role": Person.RoleChoices.ACTOR,
                "biography": "Actor icono del cine mundial, ganador de múltiples premios de la Academia.",
            },
        ]

        person_objs = {}
        for p in people_data:
            obj, _ = Person.objects.get_or_create(
                first_name=p["first_name"],
                last_name=p["last_name"],
                defaults={
                    "birth_date": p["birth_date"],
                    "primary_role": p["primary_role"],
                    "biography": p["biography"],
                },
            )
            person_objs[f"{p['first_name']} {p['last_name']}"] = obj
        self.stdout.write(self.style.SUCCESS(f"Personas verificadas: {len(person_objs)}"))

        # 3. Crear 10 Películas
        movies_data = [
            {
                "title": "Inception",
                "original_title": "Inception",
                "synopsis": "Un ladrón que roba secretos corporativos mediante tecnología de sueños compartidos recibe la tarea inversa de implantar una idea.",
                "release_year": 2010,
                "duration_minutes": 148,
                "director": person_objs["Christopher Nolan"],
                "genres": [genre_objs["Ciencia Ficción"], genre_objs["Acción"]],
                "cast": [person_objs["Leonardo DiCaprio"]],
            },
            {
                "title": "Interstellar",
                "original_title": "Interstellar",
                "synopsis": "Un equipo de exploradores viaja a través de un agujero de gusano en el espacio en un intento por asegurar la supervivencia de la humanidad.",
                "release_year": 2014,
                "duration_minutes": 169,
                "director": person_objs["Christopher Nolan"],
                "genres": [genre_objs["Ciencia Ficción"], genre_objs["Drama"]],
                "cast": [],
            },
            {
                "title": "The Dark Knight",
                "original_title": "The Dark Knight",
                "synopsis": "Cuando una amenaza conocida como el Joker desata el caos en Gotham, Batman debe someterse a una prueba física y psicológica definitiva.",
                "release_year": 2008,
                "duration_minutes": 152,
                "director": person_objs["Christopher Nolan"],
                "genres": [genre_objs["Acción"], genre_objs["Crimen / Suspenso"]],
                "cast": [person_objs["Christian Bale"]],
            },
            {
                "title": "Dune: Parte 2",
                "original_title": "Dune: Part Two",
                "synopsis": "Paul Atreides se une a Chani y a los Fremen mientras busca venganza contra los conspiradores que destruyeron a su familia.",
                "release_year": 2024,
                "duration_minutes": 166,
                "director": person_objs["Denis Villeneuve"],
                "genres": [genre_objs["Ciencia Ficción"], genre_objs["Acción"]],
                "cast": [person_objs["Timothée Chalamet"]],
            },
            {
                "title": "Blade Runner 2049",
                "original_title": "Blade Runner 2049",
                "synopsis": "Un joven blade runner de la policía de Los Ángeles descubre un secreto enterrado que podría sumir a lo que queda de la sociedad en el caos.",
                "release_year": 2017,
                "duration_minutes": 164,
                "director": person_objs["Denis Villeneuve"],
                "genres": [genre_objs["Ciencia Ficción"], genre_objs["Crimen / Suspenso"]],
                "cast": [],
            },
            {
                "title": "Taxi Driver",
                "original_title": "Taxi Driver",
                "synopsis": "Un veterano de la guerra de Vietnam mentalmente inestable trabaja como taxista nocturno en la decadente ciudad de Nueva York.",
                "release_year": 1976,
                "duration_minutes": 114,
                "director": person_objs["Martin Scorsese"],
                "genres": [genre_objs["Drama"], genre_objs["Crimen / Suspenso"]],
                "cast": [person_objs["Robert De Niro"]],
            },
            {
                "title": "Goodfellas",
                "original_title": "Goodfellas",
                "synopsis": "La historia real de Henry Hill y su vida en la mafia italoamericana junto a sus socios Tommy DeVito y Jimmy Conway.",
                "release_year": 1990,
                "duration_minutes": 145,
                "director": person_objs["Martin Scorsese"],
                "genres": [genre_objs["Crimen / Suspenso"], genre_objs["Drama"]],
                "cast": [person_objs["Robert De Niro"]],
            },
            {
                "title": "Pulp Fiction",
                "original_title": "Pulp Fiction",
                "synopsis": "Las vidas de dos sicarios, un boxeador, un gánster y su esposa se entrelazan en cuatro historias de violencia y redención.",
                "release_year": 1994,
                "duration_minutes": 154,
                "director": person_objs["Quentin Tarantino"],
                "genres": [genre_objs["Crimen / Suspenso"], genre_objs["Drama"]],
                "cast": [],
            },
            {
                "title": "El Viaje de Chihiro",
                "original_title": "Sen to Chihiro no Kamikakushi",
                "synopsis": "Una niña de diez años queda atrapada en un mundo mágico de dioses y espíritus, y debe trabajar para liberar a sus padres.",
                "release_year": 2001,
                "duration_minutes": 125,
                "director": person_objs["Hayao Miyazaki"],
                "genres": [genre_objs["Animación"], genre_objs["Drama"]],
                "cast": [],
            },
            {
                "title": "El Niño y la Garza",
                "original_title": "Kimitachi wa Dō Ikiru ka",
                "synopsis": "Durante la Segunda Guerra Mundial, un joven descubre una misteriosa torre abandonada que lo conduce a un fascinante mundo alterno.",
                "release_year": 2023,
                "duration_minutes": 124,
                "director": person_objs["Hayao Miyazaki"],
                "genres": [genre_objs["Animación"], genre_objs["Drama"]],
                "cast": [],
            },
        ]

        created_movies = {}
        for m in movies_data:
            movie_obj, _ = Movie.objects.get_or_create(
                title=m["title"],
                defaults={
                    "original_title": m["original_title"],
                    "synopsis": m["synopsis"],
                    "release_year": m["release_year"],
                    "duration_minutes": m["duration_minutes"],
                    "director": m["director"],
                },
            )
            movie_obj.genres.set(m["genres"])
            if m["cast"]:
                movie_obj.cast.set(m["cast"])
            created_movies[m["title"]] = movie_obj
        self.stdout.write(self.style.SUCCESS(f"Películas creadas o verificadas: {len(created_movies)}"))

        # 4. Crear Valoraciones (Ratings) en al menos 5 películas
        ratings_data = [
            # Inception (Promedio 9.5)
            {"movie": "Inception", "author": "Roger Ebert Site", "score": 10, "comment": "Obra maestra del cine de ciencia ficción con un montaje sobresaliente."},
            {"movie": "Inception", "author": "Film Reviewer", "score": 9, "comment": "Concepto fascinante y efectos visuales revolucionarios."},

            # Interstellar (Promedio 9.0)
            {"movie": "Interstellar", "author": "Science & Cinema", "score": 9, "comment": "Banda sonora inolvidable de Hans Zimmer y gran rigor científico emocional."},
            {"movie": "Interstellar", "author": "Cosmic Reviews", "score": 9, "comment": "Una de las mejores odiseas espaciales de todos los tiempos."},

            # The Dark Knight (Promedio 10.0)
            {"movie": "The Dark Knight", "author": "Empire Magazine", "score": 10, "comment": "Heath Ledger brinda una de las actuaciones más legendarias del cine."},
            {"movie": "The Dark Knight", "author": "Total Film", "score": 10, "comment": "El pináculo del cine de superhéroes y crimen urbano."},

            # Dune: Parte 2 (Promedio 9.5)
            {"movie": "Dune: Parte 2", "author": "Cinephile Hub", "score": 10, "comment": "Escala monumental y narrativa impecable. Villeneuve se corona como maestro moderno."},
            {"movie": "Dune: Parte 2", "author": "Screen Weekly", "score": 9, "comment": "Experiencia audiovisual inmersiva sin precedentes."},

            # Taxi Driver (Promedio 9.0)
            {"movie": "Taxi Driver", "author": "Classic Cinema Journal", "score": 9, "comment": "Retrato descarnado de la soledad y la alienación urbana."},

            # Goodfellas (Promedio 9.5)
            {"movie": "Goodfellas", "author": "Rolling Stone", "score": 10, "comment": "Ritmo frenético y dirección ejemplar del maestro Scorsese."},
            {"movie": "Goodfellas", "author": "The Guardian", "score": 9, "comment": "Pionera en la narrativa moderna de historias de mafias."},

            # El Viaje de Chihiro (Promedio 10.0)
            {"movie": "El Viaje de Chihiro", "author": "Anime Insider", "score": 10, "comment": "Poesía visual y emotiva sin igual, una cumbre de la animación universal."},
        ]

        # Limpiar ratings existentes para evitar duplicados en re-ejecución
        Rating.objects.all().delete()
        for r in ratings_data:
            Rating.objects.create(
                movie=created_movies[r["movie"]],
                author=r["author"],
                score=r["score"],
                comment=r["comment"],
            )
        self.stdout.write(self.style.SUCCESS(f"Valoraciones creadas: {len(ratings_data)}"))
        self.stdout.write(self.style.SUCCESS("Poblado de datos finalizado con éxito."))
