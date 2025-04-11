from django.db import models
from visiteur.models import ClVisiteur
from directeur.models import ClDirecteur

class ClVisite(models.Model):
    STATUT_CHOICES = [
        ('confirmé', 'Confirmé'),
        ('annulé', 'Annulé'),
    ]

    idvstr = models.ForeignKey(ClVisiteur, on_delete=models.CASCADE, verbose_name="Visiteur")
    iddirecteur = models.ForeignKey(ClDirecteur, on_delete=models.CASCADE)
    
    # OBJET et DESCRIPTION deviennent des paragraphes
    tobjt = models.TextField(null=False, verbose_name="Objet")
    ttvst = models.TextField(null=False, verbose_name="Description de la visite")

    ddvst = models.DateField(null=False, verbose_name="Date de visite")
    hvst = models.TimeField(null=True, blank=True, verbose_name="Heure de visite")
    
    tsttvst = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='confirmé',
        verbose_name="Statut de la visite"
    )
    
    # MOTIF devient aussi un paragraphe
    tmtf = models.TextField(blank=True, verbose_name="Motif")

    def save(self, *args, **kwargs):
        if self.tsttvst == 'annulé' and not self.tmtf:
            self.tmtf = "visiteur visité annulé"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Visite de {self.idvstr.tnm} {self.idvstr.tpm} avec {self.iddirecteur.tnm} {self.iddirecteur.tpm} le {self.ddvst}"
