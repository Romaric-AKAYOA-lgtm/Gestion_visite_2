from django.db import models

from directeur.models import ClDirecteur
from secretaire.models import ClSecretaire
from django.utils import timezone

class CLMutation(models.Model):
    secretaire = models.ForeignKey(ClSecretaire, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Clé étrangère vers ClDirecteur
    directeur = models.ForeignKey(ClDirecteur, on_delete=models.SET_NULL, null=True, blank=True)
    dsb = models.DateField(default=timezone.now, null=True, blank=True)
    ddf = models.DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.tnm} {self.tpm} - Secrétaire"
