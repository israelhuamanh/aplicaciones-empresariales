from .models import Category

def global_categories(request):
    """
    Context processor para que la lista de categorías esté siempre
    disponible en la barra lateral (sidebar) y barra de navegación
    sin tener que pasarla manualmente en cada vista.
    """
    return {
        'all_categories': Category.objects.all()
    }
