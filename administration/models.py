from django.db import models

class Administration(models.Model):
    nom = models.CharField(max_length=255)
    structure_superieure = models.CharField(max_length=255, blank=True, null=True)
    type_structure = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    boite_postale = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=255)
    localisation = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    devise = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    devise_pays = models.CharField(max_length=50)
    drapeau = models.ImageField(upload_to='drapeaux/')
