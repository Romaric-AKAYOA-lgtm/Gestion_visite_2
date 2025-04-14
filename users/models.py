from django.db import models
from django.utils import timezone
from datetime import date, timedelta

class ClUser(models.Model):
    SEX_CHOICES = [
        ('Masculin', 'Masculin'),
        ('Feminin', 'Féminin'),
    ]
    
    tnm = models.CharField(max_length=50, null=False)
    tpm = models.CharField(max_length=50, blank=True, null=True)
    tsx = models.CharField(max_length=10, choices=SEX_CHOICES, default='Masculin', null=False)
    dns = models.DateField(null=False)  # Date de naissance
    date_retraite = models.DateField(null=True, blank=True)  # ✅ Date de retraite calculée
    tlns = models.CharField(max_length=50, blank=True, null=True)
    tads = models.CharField(max_length=50, blank=True, null=True)
    teml = models.EmailField(blank=True, null=True, unique=True)
    tphne = models.CharField(max_length=20, blank=True, null=True, unique=True)
    dsb = models.DateField(default=timezone.now, null=True, blank=True)
    ddf = models.DateField(blank=True, null=True)
    tstt = models.CharField(max_length=50, null=True, blank=True)
    ttvst = models.CharField(max_length=50, null=False)
    img = models.ImageField(
        upload_to='user_images/',
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Calcul de la date de retraite si non définie
        if self.dns and not self.date_retraite:
            self.date_retraite = date(self.dns.year + 60, self.dns.month, self.dns.day)
        
        if not self.tstt:
            self.tstt = 'default_value'
        super(ClUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} {self.tstt}"

    def get_age(self):
        today = date.today()
        return today.year - self.dns.year - ((today.month, today.day) < (self.dns.month, self.dns.day))

    def is_over_60(self):
        return self.get_age() >= 60
