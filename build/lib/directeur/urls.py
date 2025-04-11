from django.urls import path
from . import views

app_name = 'directeur'

urlpatterns = [
    # Page d'accueil pour la gestion des directeurs
    path('', views.directeur_list, name='directeur_list'),

    # Consultation des informations d'un directeur
    path('detail/<int:id>/', views.directeur_detail, name='directeur_detail'),

    # Création d'un nouveau directeur
    path('create/', views.directeur_create, name='directeur_create'),

    # Modification des informations d'un directeur
    path('update/<int:id>/', views.directeur_update, name='directeur_update'),

    # Recherche des directeurs
    path('search/', views.directeur_search, name='directeur_search'),
    
    path('search/', views.directer_search, name='directeur_search1'),  # Cette URL doit correspondre à l'action du formulaire

    # Impression des informations d'un ou plusieurs directeurs
    path('impression/', views.directeur_impression, name='directeur_impression'),
        # Recherche des visiteurs
    # Autres URL patterns
   path('generate_word/', views.generate_word, name='generate_word')

]
