from django import forms

from secretaire.models import ClSecretaire
from users.forms import ClUserForm

# Formulaire pour ClSecretaire héritant de ClUserForm
class ClSecretaireForm(ClUserForm):
    class Meta:
        model = ClSecretaire
        fields = ClUserForm.Meta.fields + ['tstt', 'directeur']  # Ajout du champ directeur
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # Appel du constructeur de la classe parente (ClUserForm)
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'secretaire' par défaut si ce n'est pas déjà spécifié
        if not self.instance.pk and not self.instance.tstt:
            self.instance.tstt = 'secretaire'
