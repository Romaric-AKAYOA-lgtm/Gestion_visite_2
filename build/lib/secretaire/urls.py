from django.urls import path
from . import views

app_name = 'secretaire'

urlpatterns = [
    # Page d'accueil pour la gestion des secrétaires
    path('', views.secretaire_list, name='secretaire_list'),

    # Consultation des informations d'un secrétaire
    path('detail/<int:id>/', views.secretaire_detail, name='secretaire_detail'),

    # Création d'un nouveau secrétaire
    path('create/', views.secretaire_create, name='secretaire_create'),

    # Modification des informations d'un secrétaire
    path('update/<int:id>/', views.secretaire_update, name='secretaire_update'),

    # Recherche des secrétaires
    path('search/', views.secretaire_search, name='secretaire_search'),
     path('search/', views.secreter_search, name='directeur_search1'),  # Cette URL doit correspondre à l'action du formulaire

    # Impression des informations d'un ou plusieurs secrétaires
    path('impression/', views.secretaire_impression, name='secretaire_impression'),
    path('generate_word/', views.generate_word, name='generate_word')
]
