from django.urls import path
from . import views

app_name = 'mutation'

urlpatterns = [
    # Page d'accueil pour la gestion des mutations
    path('', views.mutation_list, name='mutation_list'),

    # Consultation des informations d'une mutation
    path('detail/<int:id>/', views.mutation_detail, name='mutation_detail'),

    # Création d'une nouvelle mutation
    path('create/', views.mutation_create, name='mutation_create'),

    # Modification des informations d'une mutation
    path('update/<int:id>/', views.mutation_update, name='mutation_update'),

    # Recherche des mutations
    path('search/', views.mutation_search, name='mutation_search'),

    # Impression des informations d'une ou plusieurs mutations
    path('impression/', views.mutation_impression, name='mutation_impression'),

    # Génération d'un fichier Word contenant les mutations
    path('generate_word/', views.generate_word, name='generate_word')
]
