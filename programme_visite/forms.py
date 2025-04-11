from django import forms
from .models import ClProgrammeVisite
from django.core.exceptions import ValidationError
from datetime import time, timedelta
from django.utils import timezone

class ClProgrammeVisiteForm(forms.ModelForm):
    class Meta:
        model = ClProgrammeVisite
        fields = ['idvst', 'ddpvst', 'hdbt', 'hhf', 'tsttpvst', 'motif', 'secretaire']
        widgets = {
            'ddpvst': forms.DateInput(attrs={'type': 'date'}),
            'hdbt': forms.TimeInput(attrs={'type': 'time'}),
            'hhf': forms.TimeInput(attrs={'type': 'time'}),
            'tsttpvst': forms.Select(choices=ClProgrammeVisite.STATUT_CHOICES),
            'motif': forms.Select(choices=ClProgrammeVisite.MOTIF_CHOICES),
            'secretaire': forms.Select(),
        }

    def clean_hdbt(self):
        hdbt = self.cleaned_data.get('hdbt')
        if hdbt:
            # Vérification de l'heure de début
            if hdbt < time(8, 0) or hdbt > time(14, 0):
                raise ValidationError("L'heure de début doit être comprise entre 08:00 et 14:00.")
        return hdbt

    def clean_hhf(self):
        hhf = self.cleaned_data.get('hhf')
        if hhf:
            # Vérification de l'heure de fin
            if hhf < time(8, 0) or hhf > time(14, 0):
                raise ValidationError("L'heure de fin doit être comprise entre 08:00 et 14:00.")
        return hhf

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('tsttpvst')
        motif = cleaned_data.get('motif')
        ddpvst = cleaned_data.get('ddpvst')

        # Vérification du motif si le statut est 'annulé'
        if statut == 'annulé':
            if not motif:
                self.add_error('motif', "Le motif est obligatoire si le statut est 'Annulé'.")
            
            # Si le statut est "annulé", conserver la date et la reporter au jour suivant
            if ddpvst:
                # Report de la visite au jour suivant tout en maintenant la même heure
                next_day = ddpvst + timedelta(days=1)
                cleaned_data['ddpvst'] = next_day
                self.add_error('ddpvst', f"Visite annulée, reportée au {next_day.strftime('%Y-%m-%d')}.")

        return cleaned_data
