from django.db import models

from directeur.models import ClDirecteur
from users.models import ClUser

class ClSecretaire(ClUser):
    def save(self, *args, **kwargs):
        self.tstt = "Secretaire"
        super().save(*args, **kwargs)
    # Clé étrangère vers ClDirecteur
    directeur = models.ForeignKey(ClDirecteur, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tnm} {self.tpm} - Secrétaire"
