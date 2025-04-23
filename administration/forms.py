from django import forms
from .models import Administration

class AdministrationForm(forms.ModelForm):
    class Meta:
        model = Administration
        fields = [
            'nom',
            'structure_superieure',
            'type_structure',
            'adresse',
            'ville',
            'boite_postale',
            'email',
            'localisation',
            'logo',
            'devise',
            'pays',
            'devise_pays',
            'drapeau'
        ]
