from django.urls import path
from . import views

app_name = 'visiteur'

urlpatterns = [
    # Page d'accueil pour la gestion des visiteurs
    path('', views.visiteur_list, name='visiteur_list'),

    # Consultation des informations d'un visiteur
    path('detail/<int:id>/', views.visiteur_detail, name='visiteur_detail'),

    # Création d'un nouveau visiteur
    path('create/', views.visiteur_create, name='visiteur_create'),

    # Modification des informations d'un visiteur
     path('update/<int:id>/', views.visiteur_update, name='visiteur_update'),

    # Recherche des visiteurs
    path('search/', views.visiteur_search, name='visiteur_search'),
    path('search/', views.visiter_search, name='visiteur_search1'),  # Cette URL doit correspondre à l'action du formulaire

    # Impression des informations d'un ou plusieurs visiteurs
    path('impression/', views.visiteur_impression, name='visiteur_impression'),
        # Autres URL patterns
   path('generate_word/', views.generate_word, name='generate_word')

]
