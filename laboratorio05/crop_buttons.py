import os
from PIL import Image

def crop_bottom(img_path, out_path, crop_height=300):
    with Image.open(img_path) as img:
        w, h = img.size
        # recortar los ultimos crop_height pixels
        box = (0, max(0, h - crop_height), w, h)
        cropped = img.crop(box)
        cropped.save(out_path)

if os.path.exists("screenshots/06_admin_formulario_inlines_auditoria.png"):
    crop_bottom("screenshots/06_admin_formulario_inlines_auditoria.png", "screenshots/07_admin_botones_superuser.png", 250)

if os.path.exists("screenshots/09_editor_formulario_sin_eliminar.png"):
    crop_bottom("screenshots/09_editor_formulario_sin_eliminar.png", "screenshots/10_editor_botones_sin_eliminar.png", 250)

print("Recortes generados exitosamente.")
