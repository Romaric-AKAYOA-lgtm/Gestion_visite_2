from django import forms
from django.utils.timezone import now
from datetime import timedelta
from .models import ClUser

class ClUserForm(forms.ModelForm):
    class Meta:
        model = ClUser
        fields = ['tnm', 'tpm', 'tsx', 'dns', 'tlns', 'tads', 'teml', 'tphne', 'dsb', 'ddf', 'tstt','ttvst', 'img']
        widgets = {
            'dns': forms.DateInput(attrs={'type': 'date'}),
            'dsb': forms.DateInput(attrs={'type': 'date'}),
            'ddf': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClUserForm, self).__init__(*args, **kwargs)
        # Préremplir la date de début avec la date système si elle n’est pas fournie
        if not self.initial.get('dsb'):
            self.fields['dsb'].initial = now().date()

    def clean_tnm(self):
        tnm = self.cleaned_data.get('tnm')
        if not tnm:
            raise forms.ValidationError("Le nom ne peut pas être vide.")
        if any(char.isdigit() for char in tnm):
            raise forms.ValidationError("Le nom ne doit pas contenir de chiffres.")
        return tnm

    def clean_tpm(self):
        tpm = self.cleaned_data.get('tpm')
        if tpm and any(char.isdigit() for char in tpm):
            raise forms.ValidationError("Le prénom ne doit pas contenir de chiffres.")
        return tpm

    def clean(self):
        cleaned_data = super().clean()
        dns = cleaned_data.get('dns')
        dsb = cleaned_data.get('dsb')

        if dns and dsb:
            delta = dsb - dns
            if delta < timedelta(days=28 * 365):  # Approximativement 28 ans
                self.add_error('dsb', "L'utilisateur doit avoir au moins 28 ans à la date de début.")
