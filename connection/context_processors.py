from django.contrib.auth import authenticate
from connection.models import ClConnection

def get_user_info_from_session(request):
    """Récupère les informations de l'utilisateur depuis la session."""
    
    # Récupérer le nom d'utilisateur depuis la session
    username = request.session.get('username', None)
    
    if not username:
        return None  # Aucun utilisateur trouvé dans la session
    
    # Essayons de récupérer les données de l'utilisateur via le modèle Django User
    try:
        # Essayer de récupérer l'utilisateur de ClConnection
        user_info = ClConnection.objects.get(username=username)
        
        # Récupérer le nom, prénom, statut et image si l'utilisateur existe
        user_data = {
            'username': user_info.username,
            'nom': user_info.user.tnm,  # Assurez-vous que vous avez le bon modèle lié
            'prenom': user_info.user.tpm,  # Assurez-vous que vous avez le bon modèle lié
            'statut': user_info.user.tstt,  # Assurez-vous que vous avez le bon modèle lié
            'image': user_info.user.img.url if user_info.user.img else None  # Image de profil
        }
        
        return user_data
    
    except ClConnection.DoesNotExist:
        return None  # Aucun utilisateur trouvé dans ClConnection
    except Exception as e:
        return {'error': str(e)}  # En cas d'erreur
