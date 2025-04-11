from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('list/', views.administration_list, name='list'),  # Ajout de l'URL pour la liste
  path('detail/<int:id>/', views.administration_detail, name='detail'),  # Détail d'une administration, avec id dynamique
    path('create/', views.administration_create, name='create'),
    path('modify/<int:id>/', views.administration_modify, name='modify'),  # Ajout de la route pour modifier
]
