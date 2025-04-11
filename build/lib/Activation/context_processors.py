# context_processors.py
from .models import Activation

def check_activation(request):
    """
    Vérifie si l'activation est valide avant de rendre le contexte.
    Si l'activation est invalide ou inexistante, le contexte contiendra une variable 'activation_invalid'.
    """
    try:
        # Récupérer la première activation enregistrée dans la base de données
        activation = Activation.objects.first()

        # Vérifier si l'activation est valide
        if not activation or not activation.is_valid():
            # Retourner un indicateur pour dire que l'activation est invalide
            return {'activation_invalid': True}
        return {}  # Retourne un dictionnaire vide si l'activation est valide
    except Activation.DoesNotExist:
        # Si aucune activation n'existe, considérer comme invalide
        return {'activation_invalid': True}
