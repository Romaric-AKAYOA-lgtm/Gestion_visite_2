from django import forms
from django.utils import timezone
from .models import CLMutation

class CMutationForm(forms.ModelForm):
    class Meta:
        model = CLMutation
        fields = ['secretaire', 'directeur', 'dsb', 'ddf']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()

        # Filtrer les secrétaires dont ddf est null ou > aujourd'hui
        self.fields['secretaire'].queryset = self.fields['secretaire'].queryset.filter(
            ddf__isnull=True
        ) | self.fields['secretaire'].queryset.filter(ddf__gt=today)

        # Filtrer les directeurs dans les mêmes conditions
        self.fields['directeur'].queryset = self.fields['directeur'].queryset.filter(
            ddf__isnull=True
        ) | self.fields['directeur'].queryset.filter(ddf__gt=today)

    def clean(self):
        cleaned_data = super().clean()
        secretaire = cleaned_data.get('secretaire')
        directeur = cleaned_data.get('directeur')
        dsb = cleaned_data.get('dsb')
        ddf = cleaned_data.get('ddf')

        # Vérification logique des dates
        if dsb and ddf and ddf < dsb:
            self.add_error('ddf', "La date de fin doit être postérieure à la date de début.")

        return cleaned_data
