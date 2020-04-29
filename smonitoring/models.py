from django.db import models

PEPFAR_CHOICES= [('oui','Oui'),('non','Non')]
FAI_CHOICES= [('digicel','Digicel'),('natcom','Natcom'),('access','Access Haiti'),('hainet','Hainet SA')]
EL_CHOICES= [('up','Up'),('down','Down'),('none','Non installe')]
# Create your models here.
class Site(models.Model):
	code = models.CharField(max_length=10,unique=True)
	type_site = models.CharField(max_length=10)
	nom = models.CharField(max_length=100)
	sigle = models.CharField(max_length=10, default=None, blank=True,null=True)
	region = models.CharField(max_length=100)
	departement = models.CharField(max_length=30)
	commune = models.CharField(max_length=100)
	adresse = models.CharField(max_length=100, default=None, blank=True,null=True)
	pepfar = models.CharField(max_length=10, choices = PEPFAR_CHOICES)
	contact_1 = models.CharField(max_length=100)
	tel_1 = models.CharField(max_length=100)
	contact_2 = models.CharField(max_length=100, default=None, blank=True,null=True)
	tel_2 = models.CharField(max_length=100, default=None, blank=True,null=True)
	fai = models.CharField(max_length=100, choices= FAI_CHOICES)
	internet = models.CharField(max_length=15, choices = EL_CHOICES)
	isante = models.CharField(max_length=15, choices = EL_CHOICES)
	fingerprint = models.CharField(max_length=15, choices = EL_CHOICES)

	def __str__(self):
		return f"{self.nom} ({self.code})"
"""
class Poste(models.Model):
	nom_poste = models.CharField(max_length=100)
	categorie_poste = models.CharField(max_length=100)
	domaine_poste = models.CharField(max_length=100)
	dept = models.CharField(max_length=100)
	
	def __init__(self,nom_poste,categorie_poste,domaine_poste,dept):
		self.nom_poste = nom_poste
		self.categorie_poste = categorie_poste
		self.domaine_poste = domaine_poste
		self.dept = dept

class Employe(models.Model):
	code_emp = models.CharField(max_length=100)
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	poste = models.CharField(max_length=100)
	adresse = models.CharField(max_length=100)
	tel_perso = models.CharField(max_length=100)
	tel_travail = models.CharField(max_length=100)
	bureau_affecte = models.ForeignKey(Site, on_delete=models.CASCADE)
"""
