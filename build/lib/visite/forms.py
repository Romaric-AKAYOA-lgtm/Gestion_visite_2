from django import forms
from django.core.exceptions import ValidationError
from datetime import time

from programme_visite.models import ClProgrammeVisite
from visite.models import ClVisite

class ClVisiteForm(forms.ModelForm):
    class Meta:
        model = ClVisite
        fields = ['idvstr', 'iddirecteur', 'tobjt', 'ttvst', 'ddvst', 'hvst', 'tsttvst', 'tmtf']
        widgets = {
            'ddvst': forms.DateInput(attrs={'type': 'date'}),
            'tobjt': forms.TextInput(attrs={'placeholder': 'Objet de la visite'}),
            'ttvst': forms.TextInput(attrs={'placeholder': 'Type de visiteur'}),
            'tmtf': forms.TextInput(attrs={'placeholder': 'Motif d\'annulation si nécessaire'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('tsttvst')
        motif = cleaned_data.get('tmtf')
        ddvst = cleaned_data.get('ddvst')
        hvst = cleaned_data.get('hvst')

        # Vérification du motif si le statut est 'annulé'
        if statut == 'annulé' and not motif:
            cleaned_data['tmtf'] = "visiteur visité annulé"  # Motif par défaut

        # Vérification de l'heure de la visite (doit être entre 8h et 14h)
        if hvst and (hvst < time(8, 0) or hvst > time(14, 0)):
            raise ValidationError("L'heure de la visite doit être comprise entre 8h et 14h.")

        # Vérifier si une autre visite confirmée existe pour cette même date et heure
        if ddvst and hvst:
            # Vérifier qu'il n'y a pas déjà une visite confirmée à cette date et heure
            existing_visite = ClVisite.objects.filter(
                ddvst=ddvst,
                hvst=hvst,
                tsttvst='confirmé'
            ).exclude(id=self.instance.id if self.instance.id else None)  # Exclure la visite courante en modification

            if existing_visite.exists():
                raise ValidationError(f"Il y a déjà une visite confirmée à {hvst} le {ddvst}.")

        # Vérifier si la visite est déjà utilisée dans ClProgrammeVisite et empêcher la modification de la date et heure
        if self.instance.id:  # Si la visite est déjà existante (modification)
            # Vérifier si la visite est déjà dans ClProgrammeVisite
            if ClProgrammeVisite.objects.filter(idvst=self.instance).exists():
                # Si la visite existe dans le programme, empêcher la modification de la date et de l'heure
                if ddvst != self.instance.ddvst or hvst != self.instance.hvst:
                    raise ValidationError("La date et l'heure de la visite ne peuvent pas être modifiées car cette visite est déjà utilisée dans le programme.")
        
        return cleaned_data
