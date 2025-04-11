from users.models import ClUser

class ClDirecteur(ClUser):
    def save(self, *args, **kwargs):
        self.tstt = "Directeur"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} - Directeur"
