from django.db import models
from django.contrib.auth.hashers import make_password

from users.models import ClUser

class ClConnection(models.Model):
    user = models.OneToOneField(ClUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Augmenter la taille pour le mot de passe haché

    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'sha1')):
            # Assurer que le mot de passe est haché avant de le sauvegarder
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
