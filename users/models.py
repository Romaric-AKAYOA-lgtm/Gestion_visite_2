from django.db import models
from django.utils import timezone

class ClUser(models.Model):
    # Choix pour le sexe
    SEX_CHOICES = [
        ('Masculin', 'Masculin'),
        ('Feminin', 'Féminin'),
    ]
    
    tnm = models.CharField(max_length=50, null=False)
    tpm = models.CharField(max_length=50, blank=True, null=True)
    tsx = models.CharField(max_length=10, choices=SEX_CHOICES, default='Masculin', null=False)
    dns = models.DateField(null=False)
    tlns = models.CharField(max_length=50, blank=True, null=True)
    tads = models.CharField(max_length=50, blank=True, null=True)
    teml = models.EmailField(blank=True, null=True, unique=True)  # Contrainte d'unicité ajoutée
    tphne = models.CharField(max_length=20, blank=True, null=True, unique=True)  # Contrainte d'unicité ajoutée
    dsb = models.DateField(default=timezone.now, null=True, blank=True)  # Null=True rend ce champ facultatif
    ddf = models.DateField(blank=True, null=True)
    tstt = models.CharField(max_length=50, null=True, blank=True)
    ttvst = models.CharField(max_length=50, null=False)
    # Champ image pour stocker une image de profil avec une image par défaut
    img = models.ImageField(
        upload_to='user_images/',
        blank=True,
        null=True,
        default='user_images/person-1824147_1280.png'  # <-- ce chemin est correct
    )


    def save(self, *args, **kwargs):
        # Assigner une valeur par défaut à 'tstt' si elle n'est pas définie
        if not self.tstt:
            self.tstt = 'default_value'  # Valeur par défaut si 'tstt' n'est pas assigné
        super(ClUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} {self.tstt}"
