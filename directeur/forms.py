from django import forms

from directeur.models import ClDirecteur
from users.forms import ClUserForm

# Formulaire pour ClDirecteur héritant de ClUserForm
class ClDirecteurForm(ClUserForm):
    class Meta:
        model = ClDirecteur    
        fields = ClUserForm.Meta.fields + ['tstt']  # Ajouter le champ tstt
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # Appel du constructeur de la classe parente (ClUserForm)
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'directeur' par défaut si ce n'est pas déjà spécifié
        if not self.instance.pk and not self.instance.tstt:
            self.instance.tstt = 'directeur'
