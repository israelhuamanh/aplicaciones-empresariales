# Laboratorio 6 — Motor de Plantillas con Django

**Curso:** Desarrollo de Aplicaciones Empresariales  
**Sección:** 4-C24-A  
**Tema:** Motor de plantillas, herencia, fragmentos reutilizables, filtros y autoescape.  
**Estudiante:** Israel Angel Huaman Huaman  
**Docente:** Michael Montgomery Rosell  

---

## 1. Descripción del Proyecto

Este proyecto implementa el **Laboratorio N° 6: Motor de plantillas con Django**, enfocado en la construcción de un portal de noticias moderno, modular y seguro. Se aplican técnicas de herencia de plantillas (`base.html`), componentes modulares reutilizables (`_article_card.html`), filtros de formato (`|date`, `|time`, `|truncatewords`), navegación dinámica mediante `{% url %}`, inyección de assets con `{% load static %}` y la verificación de la protección nativa contra inyecciones XSS (autoescape).

---

## 2. Tecnologías Empleadas

* **Python:** 3.14+ / 3.12+
* **Django:** 6.1
* **Pillow:** 12.3+ (para procesamiento de imágenes destacadas y avatares)
* **Base de datos:** SQLite3
* **Estándar:** PEP 8 en código Python, HTML5 semántico, CSS responsivo nativo sin dependencias externas pesadas.

---

## 3. Estructura del Proyecto

```text
laboratorio06/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Configuración de apps, media, static y plantillas
│   ├── urls.py               # Enrutamiento principal y servicio de media en desarrollo
│   └── wsgi.py
├── news/
│   ├── __init__.py
│   ├── admin.py              # Personalización ModelAdmin (Article, Category, Author)
│   ├── apps.py               # Registro de NewsConfig
│   ├── context_processors.py # global_categories para sidebar y navegación
│   ├── models.py             # Modelos Article, Category, Author con relaciones
│   ├── urls.py               # Rutas con nombres propios (home, category, detail)
│   ├── views.py              # Vistas de portada, listado por categoría y detalle
│   ├── tests.py              # 5 pruebas automatizadas (vistas, fragmentos, XSS)
│   ├── migrations/
│   │   └── 0001_initial.py   # Migración inicial de entidades
│   └── management/
│       └── commands/
│           ├── setup_admin.py # Creación del superusuario administrativo
│           └── seed_news.py   # Carga de 6 noticias en 3 categorías
├── templates/
│   ├── base.html             # Plantilla base con bloques: title, content, sidebar
│   └── news/
│       ├── _article_card.html      # Fragmento reutilizable de tarjeta de noticia
│       ├── home.html               # Portada con bucle for, empty y truncatewords
│       ├── category_articles.html  # Listado por categoría reutilizando fragmento
│       └── article_detail.html     # Ficha de detalle y demostración de autoescape
├── static/
│   └── css/
│       └── style.css         # Hoja de estilos del portal empresarial
├── requirements.txt
├── .gitignore
├── manage.py
└── README.md
```

---

## 4. Instalación y Puesta en Marcha

### 4.1. Clonar el repositorio y preparar el entorno virtual
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

### 4.3. Aplicar migraciones
```bash
python manage.py migrate
```

### 4.4. Crear el superusuario administrativo
```bash
python manage.py setup_admin
```
* **Usuario:** `admin`
* **Contraseña:** `adminpassword123`

### 4.5. Cargar datos iniciales
Puebla la base de datos con 3 categorías, autores y al menos 6 noticias completas:
```bash
python manage.py seed_news
```

### 4.6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```
* **Portal de Noticias (Portada):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Panel de Administración:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 5. Arquitectura del Motor de Plantillas

1. **Herencia de Plantillas (`base.html`):**
   * Define la estructura común: barra superior institucional, cabecera con navegación dinámica, área principal con dos columnas y pie de página.
   * Expone tres bloques principales para las vistas hijas: `{% block title %}`, `{% block content %}` y `{% block sidebar %}`.
2. **Fragmento Reutilizable (`templates/news/_article_card.html`):**
   * Encapsula el marcado HTML de la tarjeta de presentación de cada noticia.
   * Se incluye limpiamente mediante `{% include "news/_article_card.html" with article=article %}` tanto en la portada (`home.html`) como en el listado por categoría (`category_articles.html`), evitando duplicidad de código.
3. **Filtros y Etiquetas de Control:**
   * `{% for article in articles %}` y `{% empty %}`: Gestiona el flujo y el caso donde una categoría no tiene publicaciones.
   * `{{ article.published_date|date:"j \d\e F \d\e Y" }}`: Formateo legible de fechas en español.
   * `{{ article.summary|truncatewords:25 }}`: Recorte de texto a nivel de presentación sin alterar el modelo.
4. **Enrutamiento Limpio:**
   * Todos los enlaces utilizan la etiqueta `{% url 'news:category_articles' cat.slug %}` y `{% url 'news:article_detail' article.slug %}`, sin direcciones fijas a mano.

---

## 6. Demostración de Seguridad: Escapado Automático (Requisito 12)

Django activa por defecto la protección de **Autoescape** en todas las variables renderizadas en el motor de plantillas:
* **Prueba realizada:** En el cuerpo de una noticia se guardó texto con código HTML directo: `<script>alert('Ataque XSS');</script>` y `<b>Texto</b>`.
* **Resultado observado:** En lugar de ejecutarse el script malicioso en el navegador del usuario, Django transforma automáticamente los caracteres especiales en entidades HTML (`&lt;script&gt;`, `&lt;b&gt;`).
* **Justificación técnica:** Este mecanismo previene ataques de **Cross-Site Scripting (XSS)** garantizando que el contenido generado por usuarios o administradores no pueda alterar el árbol DOM ni secuestrar cookies de sesión.

---

## 7. Pruebas Automatizadas

El proyecto cuenta con 5 pruebas unitarias en `news/tests.py` que comprueban:
1. Renderizado de la portada con herencia (`base.html`) y fragmento (`_article_card.html`).
2. Listado por categoría con reutilización del componente modular.
3. Vista de detalle con carga de datos del autor y categorías.
4. Comprobación del escapado automático seguro contra inyección de scripts.
5. Manejo del estado vacío (`empty`) en portada cuando no hay noticias.

Para ejecutar los tests:
```bash
python manage.py test
```
Resultado:
```text
Ran 5 tests in 0.215s
OK
```
