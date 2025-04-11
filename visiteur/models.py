from django.db import models
from users.models import ClUser

class ClVisiteur(ClUser):
    def save(self, *args, **kwargs):
        self.tstt = "Visiteur"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.tnm} {self.tpm} - Visiteur"
