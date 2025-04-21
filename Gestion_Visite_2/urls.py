from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Gestion_Visite_2.views_2 import  generate_word, liste_utilisateurs, tatitistique_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path("home", views.home_view, name='home'), 
     path("statistique", tatitistique_view, name='statistique'), 
    path('liste_utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
     path('export-word/',  generate_word, name='export_word'),
   #  path('', login_view, name='login'),
   path('visiteur/', include('visiteur.urls')),  # Inclure les URLs de l'application visiteur
    path('visite/', include('visite.urls')),  # Inclure les URLs de l'application visite
    path('mutation/', include('mutation.urls')),  # Inclure les URLs de l'application visite
    path('secretaire/', include('secretaire.urls')),  # Inclure les URLs de l'application secretaire
    path('directeur/', include('directeur.urls')),  # Inclure les URLs de l'application directeur
    # Ajoutez d'autres applications ici, si nécessaire
   # path('', login_view, name='login'),  # Page de connexion
    path('programme_visite/', include('programme_visite.urls')),  # Inclure les URLs de l'application programme_visite
    path('Activation/', include('Activation.urls')),
    path('administration/', include('administration.urls')),
     path('', include('connection.urls')),  # Assurez-vous que c'est bien 'connecton'

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
