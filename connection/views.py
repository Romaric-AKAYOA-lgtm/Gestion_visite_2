# utils.py (si vous souhaitez centraliser la logique)
from connection.models import ClConnection
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from connection.forms import ClConnectionForm, LoginForm
from connection.models import ClConnection
from users.models import ClUser
from django.utils import timezone
from django.db.models import Q  
def get_connected_user(request):
    """Retourne l'utilisateur actuellement connecté à partir de la session."""
    username = request.session.get('username')
    if username:
        try:
            return ClConnection.objects.get(username=username)  # Retourne l'objet ClConnection
        except ClConnection.DoesNotExist:
            return None  # Si l'utilisateur n'existe pas, retourner None
    return None  # Si aucune session n'est active, retourner None


# Vue d'enregistrement (Inscription)
def register(request):
    # Obtenir la date actuelle
    current_date = timezone.now().date()

    # Filtrer les utilisateurs ayant une ddf None ou une ddf >= à la date actuelle
    users = ClUser.objects.filter(Q(ddf__isnull=True) | Q(ddf__gte=current_date))
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    """Vue pour l'enregistrement des nouveaux utilisateurs."""
    if request.method == 'POST':
        form = ClConnectionForm(request.POST)
        if form.is_valid():
            # Sauvegarde la nouvelle connexion
            form.save()
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('connection:login')  # Redirection vers la page de connexion
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez vérifier vos données.")
    else:
        form = ClConnectionForm()

    return render(request, 'connection/register.html', {'users':users,  'username':username,'form': form})

# Vue de déconnexion (Logout)
def logout_view(request):
    """Déconnecte l'utilisateur et supprime toutes les données de session."""
    logout(request)  # Supprimer toutes les données de session
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect("connection:login")  # Rediriger vers la page de connexion
from datetime import date

# Vue de connexion (Login)
def login_view(request):
    """Affiche la page de connexion et gère l'authentification des utilisateurs."""
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 🔹 Essayer avec Django superuser
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion superutilisateur réussie.")
                return redirect('home')

            # 🔹 Sinon, essayer avec ClConnection
            try:
                user_obj = ClConnection.objects.get(username=username)

                # 🔹 Vérifier si le mot de passe est correct
                if check_password(password, user_obj.password):

                    # 🔹 Récupérer l'utilisateur lié (ClUser)
                    cl_user = user_obj.user

                    # 🔹 Vérification de retraite
                    if cl_user.date_retraite and date.today() >= cl_user.date_retraite:
                        messages.error(request, "Accès refusé : Vous êtes à la retraite.")
                        return redirect('connection:login')

                    # 🔹 Connexion réussie
                    request.session['username'] = user_obj.username
                    request.session['password'] = password
                    messages.success(request, "Connexion utilisateur ClConnection réussie.")
                    return redirect('home')
                else:
                    messages.error(request, "Mot de passe incorrect pour l'utilisateur ClConnection.")
            except ClConnection.DoesNotExist:
                messages.error(request, "Aucun utilisateur trouvé avec ce nom.")
        else:
            messages.error(request, "Veuillez vérifier les erreurs dans le formulaire.")
    else:
        form = LoginForm()

    return render(request, 'connection/login.html', {'form': form})

def manage_connection(request):
    """Vue pour gérer les informations de connexion de l'utilisateur."""
    user_obj = get_connected_user(request)  # Récupérer l'utilisateur connecté

    if not user_obj:
        messages.error(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('connection:login')  # Redirection si l'utilisateur n'est pas connecté

    if request.method == 'POST':
        form = ClConnectionForm(request.POST, instance=user_obj)
        if form.is_valid():
            # Si un mot de passe a été modifié, le hacher avant de sauvegarder
            new_password = form.cleaned_data.get('password')
            if new_password and new_password != user_obj.password:
                form.instance.password = make_password(new_password)
            
            form.save()
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('home')  # Redirection vers la page d'accueil après mise à jour
        else:
            messages.error(request, "Erreur lors de la mise à jour de vos informations.")
    else:
        form = ClConnectionForm(instance=user_obj)

    return render(request, 'connection/manage_connection.html', {'form': form})
