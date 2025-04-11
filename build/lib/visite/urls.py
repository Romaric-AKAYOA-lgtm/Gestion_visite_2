from django.urls import path
from . import views

app_name = 'visite'

urlpatterns = [
    # Page d'accueil pour la gestion des visites
    path('', views.visite_list, name='visite_list'),

    # Consultation des informations d'une visite
    path('detail/<int:id>/', views.visite_detail, name='visite_detail'),

    # Création d'une nouvelle visite
    path('create/', views.visite_create, name='visite_create'),

    # Modification des informations d'une visite
    path('update/<int:id>/', views.visite_update, name='visite_update'),

    # Recherche des visites
    path('search/', views.visite_search, name='visite_search'),

    # Impression des informations d'une ou plusieurs visites
    path('impression/', views.visite_impression, name='visite_impression'),
    # Impression au format Word
    path('generate-word/', views.generate_word, name='generate_word'),

]
