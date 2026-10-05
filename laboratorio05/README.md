# Laboratorio 5 — Desarrollo de Aplicaciones Empresariales

**Curso:** Desarrollo de Aplicaciones Empresariales  
**Sección:** 4-C24-A  
**Tema:** Administrador con Django, modelos relacionados, auditoría, permisos y recomendaciones.  

---

## 1. Descripción del Proyecto

Este proyecto implementa de manera autónoma y completa el **Laboratorio 5: Administrador con Django**. Se enfoca en la gestión de un catálogo cinematográfico con modelos interrelacionados (`Movie`, `Genre`, `Person`, `Rating`), la personalización avanzada del panel administrativo `django.contrib.admin`, la gestión granular de accesos por roles (superusuario vs. grupo `editores`) y la publicación de una vista web para recomendaciones ordenadas por valoración y filtrables por género.

---

## 2. Tecnologías Empleadas

* **Python:** 3.12+ (Ejecutado con Python 3.14)
* **Django:** 6.1
* **Pillow:** 12.3+ (para procesamiento y almacenamiento de imágenes/pósteres)
* **Base de datos:** SQLite3
* **Estándar:** PEP 8 en código Python, HTML5 semántico y CSS responsivo moderno.

---

## 3. Estructura del Proyecto

```text
laboratorio5/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Configuración, apps, media y localización
│   ├── urls.py               # Enrutamiento raíz, /admin/, /movies/ y media
│   └── wsgi.py
├── movies/
│   ├── __init__.py
│   ├── admin.py              # Personalización ModelAdmin, inlines, filtros, auditoría
│   ├── apps.py               # Configuración de MoviesConfig
│   ├── models.py             # Modelos Movie, Genre, Person, Rating
│   ├── urls.py               # Rutas de recomendaciones y detalle
│   ├── views.py              # Vista de recomendaciones (agregaciones ORM) y detalle
│   ├── tests.py              # 10 tests automatizados (modelos, vistas, permisos)
│   ├── migrations/
│   │   ├── 0001_initial.py   # Migración inicial de los 4 modelos
│   │   └── __init__.py
│   ├── management/
│   │   └── commands/
│   │       ├── seed_data.py   # Script de poblado (10 películas, 5 géneros, valoraciones)
│   │       └── setup_roles.py # Creación de superusuario, grupo editores y permisos
│   └── templates/
│       └── movies/
│           ├── base.html             # Plantilla base con barra de navegación
│           ├── recommendations.html  # Vista pública de películas mejor valoradas
│           └── movie_detail.html     # Ficha técnica y críticas detalladas
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

---

## 4. Instalación y Puesta en Marcha

### 4.1. Clonar el repositorio y preparar el entorno
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 4.2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4.3. Ejecutar migraciones
```bash
python manage.py migrate
```

### 4.4. Configurar usuarios, roles y permisos
Ejecuta el comando automatizado que crea el superusuario, el grupo `editores` y el usuario editor de prueba:
```bash
python manage.py setup_roles
```
* **Superusuario:**
  * Usuario: `admin`
  * Contraseña: `adminpassword123`
  * Rol: Acceso total al sistema y panel.
* **Usuario Editor:**
  * Usuario: `editor1`
  * Contraseña: `editorpassword123`
  * Rol: Miembro del grupo `editores` (`is_staff=True`), puede añadir y modificar películas pero **NO** eliminarlas.

### 4.5. Cargar datos de prueba
Puebla la base de datos con 10 películas reales, 5 géneros, directores/actores reconocidos y valoraciones críticas:
```bash
python manage.py seed_data
```

### 4.6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

* **Vista pública de recomendaciones:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o [http://127.0.0.1:8000/movies/](http://127.0.0.1:8000/movies/)
* **Panel de administración:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 5. Modelos de Datos y Relaciones

1. **`Genre` (Género):**
   * Campos: `name` (único), `description`, `created_at`, `updated_at`.
2. **`Person` (Persona):**
   * Campos: `first_name`, `last_name`, `birth_date`, `biography`, `primary_role` (`ACTOR`, `DIRECTOR`, `PRODUCER`, `WRITER`), `photo`, `created_at`, `updated_at`.
3. **`Movie` (Película):**
   * Campos: `title`, `original_title`, `synopsis`, `release_year`, `duration_minutes`, `poster`, `created_at`, `updated_at`.
   * **Relaciones:**
     * `genres`: `ManyToManyField(Genre, related_name="movies")`
     * `director`: `ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name="directed_movies")`
     * `cast`: `ManyToManyField(Person, blank=True, related_name="acted_movies")`
4. **`Rating` (Valoración):**
   * Campos: `author`, `score` (entero de 1 a 10), `comment`, `created_at`, `updated_at`.
   * **Relaciones:**
     * `movie`: `ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")`

---

## 6. Personalización de Django Admin

En `movies/admin.py`:
* **Gestión en Línea (`TabularInline`):** `RatingInline` permite añadir y revisar las valoraciones directamente desde el formulario de la película sin salir del registro padre.
* **Campos de Auditoría:** `created_at` y `updated_at` están marcados como `readonly_fields`, impidiendo su alteración manual y garantizando la trazabilidad.
* **Listado Mejorado (`list_display`):** Muestra columnas clave: título, año, duración, director, géneros asociados (`display_genres`), promedio de puntuación calculado (`display_average_rating`) y fecha de creación.
* **Filtros (`list_filter`):** Filtro lateral por género cinematográfico y por año de estreno.
* **Búsqueda (`search_fields`):** Búsqueda por título de la película y nombres/apellidos del director.
* **Selector Horizontal (`filter_horizontal`):** Facilita la asignación ergonómica de múltiples géneros y miembros del reparto.

---

## 7. Usuarios, Grupos y Permisos

* **Grupo `editores`:**
  * Permisos asignados:
    * `movies.add_movie` (Añadir película)
    * `movies.change_movie` (Modificar película)
    * `movies.view_movie` (Visualizar película)
    * `movies.view_genre`, `movies.view_person`, `movies.view_rating`, `movies.add_rating`, `movies.change_rating`
  * Permiso restringido / revocado:
    * **`movies.delete_movie` NO CONCEDIDO**.
* **Comprobación en el Panel:**
  * Al iniciar sesión con `editor1`, el botón rojo *"Eliminar"* desaparece del formulario de edición de la película, y la acción *"Eliminar las películas seleccionadas"* no está permitida. Intentar acceder por URL directa a la acción de borrado responde con código HTTP **403 Forbidden**.

---

## 8. Vista Pública de Recomendaciones

* **Criterio de recomendación:** Consulta películas calculando en tiempo real su promedio de valoración (`Avg('ratings__score')`) y ordenándolas de mayor a menor puntuación (`-avg_rating`, `-release_year`).
* **Filtro interactivo por género:** Permite aislar películas de un género específico (ej. Ciencia Ficción, Drama, Acción, Animación) para contrastar recomendaciones dentro de la misma categoría.
* **Ficha de Detalle:** Cada película enlaza a su vista de detalle (`/movies/<id>/`) donde se desglosan la sinopsis, reparto, datos técnicos y el listado de críticas individuales con fecha y autor.

---

## 9. Pruebas Automatizadas

El proyecto incluye 10 pruebas unitarias en `movies/tests.py` que cubren:
1. Creación de modelos y sus representaciones `__str__`.
2. Relaciones ManyToMany y ForeignKey con cálculo correcto de agregaciones (`average_rating`, `total_ratings`).
3. Auditoría de fecha de creación (`auto_now_add`).
4. Código de respuesta HTTP 200 y renderizado del template en la vista de recomendaciones.
5. Filtrado por género y ordenamiento estricto por mayor puntuación.
6. Vista de detalle de película.
7. Comprobación de permisos del grupo `editores` (`add` y `change` habilitados, `delete` deshabilitado).
8. Validación de denegación 403 Forbidden en el panel de admin al intentar eliminar con rol editor.
9. Validación de acceso total de superusuario a la eliminación.
10. Redirección y bloqueo a usuarios comunes (`is_staff=False`).

Para ejecutar los tests:
```bash
python manage.py test
```
Resultados:
```text
Ran 10 tests in ~0.5s
OK
```

---

## 10. Auditoría y Verificación de Calidad

* **Integridad del sistema:** `python manage.py check` &rarr; `0 issues`.
* **Migraciones sincronizadas:** `python manage.py makemigrations --check` &rarr; `No changes detected`.
* **Tests unitarios:** `python manage.py test` &rarr; `10 tests OK`.
