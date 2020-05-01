from django.db import models
from datetime import datetime
# Working with django user model
from django.contrib.auth.models import User


PEPFAR_CHOICES= [('oui','Oui'),('non','Non')]
FAI_CHOICES= [('digicel','Digicel'),('natcom','Natcom'),('access','Access Haiti'),('hainet','Hainet SA')]
EL_CHOICES= [('up','Up'),('down','Down'),('none','Non installe')]
RAISON_CHOICES= [('0','N/A'),('1','Problème FAI'),('2','Problème Interne'),('3','Problème non identifie'),('4','Source non identifié')]
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
	bureau_affecte = models.ForeignKey(Site, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.nom} {self.prenom}"

class Evenement(models.Model):
	code_site = models.ForeignKey(Site, on_delete= models.CASCADE, related_name="site")
	entite_concerne = models.CharField(max_length=100, choices= [('internet','Internet'),('isante','Isante Server'),('fingerprint','Fingerprint Server')]) # internet, isante or fingerprint
	status_ev = models.CharField(max_length=10, choices= EL_CHOICES) # up, down, none
	raison_ev = models.CharField(max_length=100, choices= RAISON_CHOICES)
	date_ev = models.DateField(default=datetime.now().date())
	date_rap = models.DateField(default=datetime.now().date())
	date_entree = models.DateTimeField(default=datetime.utcnow)
	pers_contact = models.CharField(max_length=100, default=None, blank=True,null=True)
	remarques = models.CharField(max_length=100, default=None, blank=True,null=True)
	code_utilisateur = models.CharField(max_length=100)
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

