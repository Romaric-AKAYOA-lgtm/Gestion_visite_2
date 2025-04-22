from django.contrib.auth.models import User
from connection.models import ClConnection

def get_user_info_from_session(request):
    """Récupère les informations de l'utilisateur depuis la session,
    que ce soit un utilisateur ClConnection ou un superutilisateur Django.
    """
    
    username = request.session.get('username', None)
    
    if not username:
        return None  # Aucun utilisateur trouvé dans la session

    # Tentative 1 : Utilisateur dans ClConnection
    try:
        user_info = ClConnection.objects.get(username=username)

        user_data = {
            'username': user_info.username,
            'nom': user_info.user.tnm,
            'prenom': user_info.user.tpm,
            'statut': user_info.user.tstt,
            'image': user_info.user.img.url if user_info.user.img else None
        }
        return user_data

    except ClConnection.DoesNotExist:
        # Tentative 2 : Vérifier si c'est un superuser Django
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                return {
                    'username': user.username,
                    'nom': user.first_name or 'Super',
                    'prenom': user.last_name or 'Utilisateur',
                    'statut': 'Superutilisateur',
                    'image': None  # ou un chemin par défaut
                }
        except User.DoesNotExist:
            return None

    except Exception as e:
        return {'error': str(e)}
