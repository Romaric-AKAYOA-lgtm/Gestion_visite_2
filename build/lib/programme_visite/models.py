from django.db import models
from visite.models import ClVisite
from secretaire.models import ClSecretaire  # Assurez-vous d'importer le modèle ClSecretaire

class ClProgrammeVisite(models.Model):
    STATUT_CHOICES = [
        ('confirmé', 'Confirmé'),
        ('annulé', 'Annulé'),
    ]

    MOTIF_CHOICES = [
        ('visiteur occupé', 'Visiteur occupé'),
        ('directeur occupé', 'Directeur occupé'),
    ]

    idvst = models.ForeignKey(ClVisite, on_delete=models.CASCADE, verbose_name="Visite")
    ddpvst = models.DateField(null=False, verbose_name="Date programmée de visite")
    hdbt = models.TimeField(null=False, verbose_name="Heure début")
    hhf = models.TimeField(null=True, blank=True, verbose_name="Heure fin")
    tsttpvst = models.CharField(
        max_length=60,
        choices=STATUT_CHOICES,
        default='confirmé',
        null=False,
        verbose_name="Statut du programme de visite"
    )
    motif = models.CharField(
        max_length=50,
        choices=MOTIF_CHOICES,
        blank=True,
        verbose_name="Motif (en cas d'empêchement)"
    )
    secretaire = models.ForeignKey(
        ClSecretaire,
        on_delete=models.CASCADE,
        verbose_name="Secrétaire",
        null=True,  # Si c'est optionnel, sinon mettez `null=False`
        blank=True   # Si c'est optionnel, sinon mettez `blank=False`
    )

    def save(self, *args, **kwargs):
        # Si le statut est 'annulé', le motif doit être renseigné
        if self.tsttpvst == 'annulé' and not self.motif:
            raise ValueError("Le motif est obligatoire lorsque le statut est 'Annulé'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Programme pour {self.idvst} le {self.ddpvst}"
