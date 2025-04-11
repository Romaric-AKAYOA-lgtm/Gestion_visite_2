from django import forms

from visiteur.models import ClVisiteur
from users.forms import ClUserForm

# Formulaire pour ClVisiteur héritant de ClUserForm
class ClVisiteurForm(ClUserForm):
    class Meta:
        model = ClVisiteur
        fields = ClUserForm.Meta.fields + ['tstt','ttvst']  # Ajout du champ tstt
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # Appel du constructeur de la classe parente (ClUserForm)
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.instance.tstt:
            self.instance.tstt = 'visiteur'
