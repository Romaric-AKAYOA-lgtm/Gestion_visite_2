from django import forms
from .models import ClConnection 
from django.core.exceptions import ValidationError

class ClConnectionForm(forms.ModelForm):
    class Meta:
        model = ClConnection
        fields = ['user', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'maxlength': 8}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) > 8:
            raise ValidationError("Le mot de passe ne doit pas dépasser 8 caractères.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Vérifie s'il existe déjà un enregistrement avec le même username + password
            if ClConnection.objects.filter(username=username, password=password).exists():
                raise ValidationError("Une combinaison identique de nom d'utilisateur et de mot de passe existe déjà.")
        
        return cleaned_data

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
