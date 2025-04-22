# utils.py (si vous souhaitez centraliser la logique)
from connection.models import ClConnection
from datetime import date

# views.py
from django.shortcuts import render, get_object_or_404
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
from django.contrib.auth.models import User  # Import du modèle User de Django

def get_connected_user(request):
    """Retourne l'utilisateur connecté à partir de ClConnection, ou le superuser s'il est connecté."""
    username = request.session.get('username')
    
    if username:
        try:
            # Vérifie si l'utilisateur est dans ClConnection
            return ClConnection.objects.get(username=username)
        except ClConnection.DoesNotExist:
            try:
                # Vérifie si c'est un superuser Django
                user = User.objects.get(username=username)
                if user.is_superuser:
                    return user  # Retourne l'utilisateur Django s’il est superutilisateur
            except User.DoesNotExist:
                return None  # Aucun utilisateur trouvé
    return None  # Aucune session active

def register(request, id=None):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    current_date = timezone.now().date()

    # Filtrer selon la situation
    if id:
        users = ClUser.objects.filter(id=id)
    else:
        users = ClUser.objects.filter(Q(ddf__isnull=True) | Q(ddf__gte=current_date))

    instance = None
    update_mode = False

    if id:
        try:
            instance = ClConnection.objects.get(pk=id)
            update_mode = True
        except ClConnection.DoesNotExist:
            user = get_object_or_404(ClUser, pk=id)
            if ClConnection.objects.filter(user=user).exists():
                messages.warning(request, "Ce compte existe déjà.")
                return redirect('connection:login')
            instance = ClConnection(user=user)

    if request.method == 'POST':
        form = ClConnectionForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if update_mode:
                messages.success(request, "Mise à jour réussie.")
            else:
                messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('connection:login')
        else:
            messages.error(request, "Erreur lors de l'enregistrement. Veuillez vérifier les champs.")
    else:
        form = ClConnectionForm(instance=instance)

    return render(request, 'connection/register.html', {
        'form': form,
        'users': users,
        'username': username,
        'update_mode': update_mode
    })

# Vue de déconnexion (Logout)
def logout_view(request):
    """Déconnecte l'utilisateur et supprime toutes les données de session."""
    logout(request)  # Supprimer toutes les données de session
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect("connection:login")  # Rediriger vers la page de connexion

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

                    # 🔹 Message avec infos utilisateur
                    messages.success(
                        request,
                        f"Bienvenue {cl_user.tnm} {cl_user.tpm} — Connexion réussie."
                    )
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

def detail_connection(request, id):
    try:
        # 🔹 Cas 1 : Essayer de récupérer une connexion ClConnection
        connection = ClConnection.objects.get(id=id)
        return render(request, 'connection/detail_connection.html', {'connection': connection})

    except ClConnection.DoesNotExist:
        try:
            # 🔹 Cas 2 : Essayer de récupérer un utilisateur ClUser sans compte
            utilisateur = ClUser.objects.get(id=id)
            messages.error(
                request,
                f"L'utilisateur {utilisateur.tnm} {utilisateur.tpm} n'a pas encore de compte."
            )
            return register(request, id=id)

        except ClUser.DoesNotExist:
            try:
                # 🔹 Cas 3 : Vérifier s'il s'agit d'un superutilisateur Django
                super_user = User.objects.get(id=id)
                if super_user.is_superuser:
                    messages.info(request, "Détails du superutilisateur Django.")
                    return render(request, 'connection/superuser_info.html', {'user': super_user})
                else:
                    messages.warning(request, "Cet utilisateur Django n'est pas un superutilisateur.")
                    return redirect('home')

            except User.DoesNotExist:
                messages.error(request, "Aucun utilisateur correspondant à cet ID.")
                return redirect('home')
