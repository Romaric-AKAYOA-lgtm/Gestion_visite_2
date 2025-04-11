from django import forms
from .models import Administration

class AdministrationForm(forms.ModelForm):
    class Meta:
        model = Administration
        fields = ['nom', 'localisation', 'logo', 'devise', 'pays', 'devise_pays', 'drapeau']  # Ajout du champ drapeau
