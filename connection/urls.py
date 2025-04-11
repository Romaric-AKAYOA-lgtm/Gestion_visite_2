from django.urls import path
from . import views

app_name = 'connection'  # Nom de l'application pour les redirections

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('manage/', views.manage_connection, name='manage'),  # Ajout de l'URL pour gérer les informations de l'utilisateur
    # Autres chemins...
]
