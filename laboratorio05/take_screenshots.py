import asyncio
from playwright.async_api import async_playwright

async def take_screenshots():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        
        # Contexto 1: Vista Pública de Recomendaciones
        context_pub = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context_pub.new_page()
        
        # 1. Recomendaciones generales
        print("Capturando 01_recomendaciones_publicas.png...")
        await page.goto("http://127.0.0.1:8000/movies/")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/01_recomendaciones_publicas.png", full_page=True)
        
        # 2. Filtrado por género (Ciencia Ficción)
        print("Capturando 02_filtro_genero.png...")
        await page.click("text=Ciencia Ficción")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/02_filtro_genero.png", full_page=True)

        # 3. Detalle de película
        print("Capturando 03_detalle_pelicula.png...")
        await page.click("text=Ver detalle →")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshots/03_detalle_pelicula.png", full_page=True)
        await context_pub.close()

        # Contexto 2: Superusuario (Admin)
        context_admin = await browser.new_context(viewport={"width": 1280, "height": 850})
        page_admin = await context_admin.new_page()
        
        print("Iniciando sesión como Superusuario (admin)...")
        await page_admin.goto("http://127.0.0.1:8000/admin/login/")
        await page_admin.fill("input[name='username']", "admin")
        await page_admin.fill("input[name='password']", "adminpassword123")
        await page_admin.click("input[type='submit']")
        await page_admin.wait_for_timeout(1000)
        
        # 4. Panel Admin Principal
        print("Capturando 04_admin_dashboard.png...")
        await page_admin.screenshot(path="screenshots/04_admin_dashboard.png")

        # 5. Lista de Películas (list_display, list_filter, search_fields)
        print("Capturando 05_admin_peliculas_personalizado.png...")
        await page_admin.goto("http://127.0.0.1:8000/admin/movies/movie/")
        await page_admin.wait_for_timeout(1000)
        await page_admin.screenshot(path="screenshots/05_admin_peliculas_personalizado.png")

        # 6. Formulario de Película (Inception) mostrando campos auditoría y RatingInline
        print("Capturando 06_admin_formulario_inlines_auditoria.png...")
        await page_admin.click("text=Inception")
        await page_admin.wait_for_timeout(1000)
        await page_admin.screenshot(path="screenshots/06_admin_formulario_inlines_auditoria.png", full_page=True)

        # 7. Zoom/Detalle de permisos de Superusuario (Botón Eliminar visible)
        print("Capturando 07_admin_permiso_eliminar_superuser.png...")
        # Captura de la parte inferior donde está el botón eliminar
        await page_admin.screenshot(path="screenshots/07_admin_permiso_eliminar_superuser.png")
        await context_admin.close()

        # Contexto 3: Usuario Editor (Grupo 'editores')
        context_editor = await browser.new_context(viewport={"width": 1280, "height": 850})
        page_editor = await context_editor.new_page()

        print("Iniciando sesión como Usuario Editor (editor1)...")
        await page_editor.goto("http://127.0.0.1:8000/admin/login/")
        await page_editor.fill("input[name='username']", "editor1")
        await page_editor.fill("input[name='password']", "editorpassword123")
        await page_editor.click("input[type='submit']")
        await page_editor.wait_for_timeout(1000)

        # 8. Dashboard del Editor (Solo ve lo asignado)
        print("Capturando 08_editor_dashboard.png...")
        await page_editor.screenshot(path="screenshots/08_editor_dashboard.png")

        # 9. Formulario del Editor en Inception (Botón Eliminar NO EXISTE)
        print("Capturando 09_editor_formulario_sin_eliminar.png...")
        await page_editor.goto("http://127.0.0.1:8000/admin/movies/movie/")
        await page_editor.wait_for_timeout(1000)
        await page_editor.click("text=Inception")
        await page_editor.wait_for_timeout(1000)
        await page_editor.screenshot(path="screenshots/09_editor_formulario_sin_eliminar.png", full_page=True)
        await context_editor.close()

        await browser.close()
        print("¡Todas las capturas de pantalla fueron tomadas con éxito!")

asyncio.run(take_screenshots())
