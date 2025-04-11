from django.urls import path
from . import views

app_name = 'programme_visite'

urlpatterns = [
    path('programme_visite/', views.programme_visite_list, name='programme_visite_list'),
    path('programme_visite/create/', views.programme_visite_create, name='programme_visite_create'),
    path('programme_visite/<int:id>/update/', views.programme_visite_update, name='programme_visite_update'),
    path('programme_visite/<int:id>/detail/', views.programme_visite_detail, name='programme_visite_detail'),
       path('programme_visite/', views.programme_visite_list, name='programme_visite_list'),
  
    # Ajouter les URLs pour imprimer
    path('programme_visite/<int:id>/imprimer/', views.imprimer_programme_visite, name='imprimer_programme_visite'),
    path('programme_visite/imprimer_liste/', views.imprimer_liste_programmes_visites, name='imprimer_liste_programmes_visites'),
    path('programme_visite/generer_word/', views.generate_word, name='generer_fichier_word'),

]
