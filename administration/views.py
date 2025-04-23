from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from connection.views import get_connected_user

from .models import Administration
from .forms import AdministrationForm
from django.shortcuts import render, get_object_or_404, redirect

def administration_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer toutes les administrations
    administrations = Administration.objects.all()
    return render(request, 'administration/administration_list.html', {'administrations': administrations, 'username':username})

def administration_detail(request, id):  # Accepte l'ID comme paramètre
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer l'administration par son ID
    administration = get_object_or_404(Administration, id=id)

    return render(request, 'administration/detail.html', {'administration': administration, 'username':username})

def administration_create(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == 'POST':
        form = AdministrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administration:list')  # Rediriger vers la page de détail après sauvegarde
    else:
        form = AdministrationForm()
    return render(request, 'administration/create.html', {'form': form, 'username':username})

def administration_modify(request, id):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer l'administration existante
    administration = get_object_or_404(Administration, id=id)

    if request.method == 'POST':
        form = AdministrationForm(request.POST, request.FILES, instance=administration)
        if form.is_valid():
            form.save()
            return redirect('administration:list')  # Rediriger vers la page de détail après modification
    else:
        form = AdministrationForm(instance=administration)

    return render(request, 'administration/administration_form.html', {'form': form, 'administration': administration, 'username':username})

