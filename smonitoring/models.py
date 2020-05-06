from django.db import models
from datetime import datetime
from django.utils import timezone as timezone
# Working with django user model
from django.contrib.auth.models import User

REGION_CHOICES= [('centre','CENTRE'),('sud','SUD'),('nord','NORD')]
DEPARTEMENT_CHOICES= [('ouest','Ouest'),('nord','Nord'),('nord-est','Nord-Est'),('nord-ouest','Nord-Ouest'),('sud','Sud'),('sud-est','Sud-Est'),('nippes','Nippes'),('centre','Centre'),('grand\'anse','Grand\'Anse')]
PEPFAR_CHOICES= [('oui','Oui'),('non','Non')]
FAI_CHOICES= [('digicel','Digicel'),('natcom','Natcom'),('access','Access Haiti'),('hainet','Hainet SA')]
EL_CHOICES= [('up','Up'),('down','Down'),('none','Non installe')]
RAISON_CHOICES= [('0','N/A'),('1','Problème FAI'),('2','Problème Interne'),('3','Problème non identifie'),('4','Source non identifié')]

# Create your models here.
class Region(models.Model):
	code= models.CharField(max_length=10,unique=True)
	nom_region = models.CharField(max_length=100)
	def __str__(self):
		return self.nom_region
	
class Departement(models.Model):
	code= models.CharField(max_length=10,unique=True)
	nom_departement = models.CharField(max_length=100)
	region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="region_ref")
	def __str__(self):
		return self.nom_departement

class Site(models.Model):
	code = models.CharField(max_length=10,unique=True)
	type_site = models.CharField(max_length=10, choices =[('site','Site'),('bureau','Bureau')])
	nom = models.CharField(max_length=100)
	sigle = models.CharField(max_length=10, default=None, blank=True,null=True)
	region = models.ForeignKey(Region,on_delete=models.CASCADE, related_name="nom_reg")
	departement = models.ForeignKey(Departement,on_delete=models.CASCADE, related_name="dept_ref")
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
		return f"{self.nom}"

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
	poste = models.ForeignKey(Poste,on_delete=models.CASCADE, related_name="desc_poste")
	adresse = models.CharField(max_length=100)
	tel_perso = models.CharField(max_length=100)
	tel_travail = models.CharField(max_length=100)
	bureau = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="bureau_ref")
	
	def __str__(self):
		return f"{self.nom} {self.prenom}"

class RaisonsEvenement(models.Model):
	code_ev=models.CharField(max_length=100)
	desc_ev=models.CharField(max_length=100)
	def __str__(self):
		return self.desc_ev
	
	
class Evenement(models.Model):
	code_site = models.ForeignKey(Site, on_delete= models.CASCADE, related_name="site")
	entite_concerne = models.CharField(max_length=100, choices= [('internet','Internet'),('isante','Isante Server'),('fingerprint','Fingerprint Server')]) # internet, isante or fingerprint
	status_ev = models.CharField(max_length=10, choices= EL_CHOICES) # up, down, none
	raison_ev = models.ForeignKey(RaisonsEvenement, on_delete=models.CASCADE, related_name="raison")
	date_ev = models.DateField(default=timezone.now)
	date_rap = models.DateField(default=timezone.now)
	date_entree = models.DateTimeField(default=timezone.now)
	pers_contact = models.CharField(max_length=100, default=None, blank=True,null=True)
	remarques = models.CharField(max_length=100, default=None, blank=True,null=True)
	nom_utilisateur = models.CharField(max_length=50)
	"""
	def __init__(self,code_site,entite_concerne,status_ev,date_ev,raison_ev,date_rap,pers_contact,remarques,date_entree,code_utilisateur):
		self.code_site=code_site
		self.entite_concerne=entite_concerne
		self.status_ev=status_ev
		self.raison_ev=raison_ev
		self.date_ev=date_ev
		self.date_rap=date_rap
		self.date_entree=date_entree
		self.pers_contact=pers_contact
		self.remarques=remarques
		self.code_utilisateur=code_utilisateur
	"""
	def __str__(self):
		return f"{self.entite_concerne} {self.status_ev} ({self.code_site})"

