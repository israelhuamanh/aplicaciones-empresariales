import asyncio
from playwright.async_api import async_playwright

async def capture_lab6():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 850})
        page = await context.new_page()

        # 1. Portada del portal (Requisitos 4, 5, 6, 10)
        print("Capturando 01_portada_noticias.png...")
        await page.goto("http://127.0.0.1:8000/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/01_portada_noticias.png", full_page=True)

        # 2. Listado por categoría (Requisito 8: reutilizando _article_card.html)
        print("Capturando 02_categoria_tecnologia.png...")
        await page.goto("http://127.0.0.1:8000/categoria/tecnologia/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/02_categoria_tecnologia.png", full_page=True)

        # 3. Ficha de detalle de noticia (Requisito 7)
        print("Capturando 03_detalle_noticia.png...")
        await page.goto("http://127.0.0.1:8000/noticia/django-6-1-revoluciona-desarrollo-aplicaciones-empresariales/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/03_detalle_noticia.png", full_page=True)

        # 4. Noticia con demostración de autoescape (Requisito 12)
        print("Capturando 04_demostracion_autoescape.png...")
        await page.goto("http://127.0.0.1:8000/noticia/prueba-escapado-automatico-django-seguridad-xss/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/04_demostracion_autoescape.png", full_page=True)

        # 5. Django Admin: Listado de Artículos (Requisito 11)
        print("Iniciando sesión en Admin...")
        await page.goto("http://127.0.0.1:8000/admin/login/")
        await page.fill("input[name='username']", "admin")
        await page.fill("input[name='password']", "adminpassword123")
        await page.click("input[type='submit']")
        await page.wait_for_timeout(1000)

        print("Capturando 05_admin_articulos.png...")
        await page.goto("http://127.0.0.1:8000/admin/news/article/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/05_admin_articulos.png")

        # 6. Django Admin: Formulario de edición con filter_horizontal
        print("Capturando 06_admin_formulario.png...")
        await page.click("text=Django 6.1 revoluciona")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/06_admin_formulario.png", full_page=True)

        await browser.close()
        print("¡Capturas de pantalla del Laboratorio 6 completadas con éxito!")

asyncio.run(capture_lab6())
