
# context_processors.py

from .models import Administration

def administration(request):
    try:
        # Vous pouvez personnaliser la récupération de l'administration ici (par exemple, en prenant le premier objet)
        administration = Administration.objects.first()  # Ou votre logique spécifique pour obtenir l'objet administration
        return {'administration': administration}
    except Administration.DoesNotExist:
        return {'administration': None}
