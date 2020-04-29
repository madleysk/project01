from django.db import models
from django.forms import ModelForm
from .models import Site
#from django import Form

"""
class RegistrationForm(Form):
	username = forms.CharField(max_length=100)
	passwd = forms.PasswordField()
	pwd_confirm = forms.PasswordField()
	auth_level = forms.HiddenField()
	code = forms.CharField(required=True)

class LoginForm(Form):
	username = forms.CharField(max_length=100)
	passwd = forms.PasswordField()
"""
class SiteForm(ModelForm):
	class Meta:
		model = Site
		fields = ['code','type_site','nom','sigle','region','departement'\
		,'commune','adresse','pepfar','contact_1','tel_1','contact_2',\
		'tel_2','fai','internet','isante','fingerprint']
	
"""
class EmployeForm(Form):
	code_emp= StringField('Code',[validators.Length(min=2,max=10)])
	nom= StringField('Nom',[validators.Length(min=2,max=60)])
	prenom= StringField('Prenom',[validators.Length(min=2,max=60)])
	email= EmailField('Adresse Email',[validators.DataRequired(message='Enter a valid email.')])
	poste= SelectField('Poste',validate_choice=False)
	adresse= StringField('Adresse Postale',[validators.Length(min=2,max=60)])
	tel_perso= TelField('Telephone Perso',[validators.Length(min=8,max=15)])
	tel_travail= TelField('Telephone Travail',[validators.Length(min=8,max=15)])
	bureau_affecte= SelectField('Bureau Affectation',validate_choice=False)
	
class EvenementForm(Form):
	code_site= SelectField('Site',[validators.DataRequired()])
	entite_concerne= SelectField('Element',[validators.DataRequired()],choices=[('','Selectionner'),('internet','Internet'),('isante','iSante Servveur'),('fingerprint','Fingerprint Servveur')])
	status_ev= SelectField(u'Status',[validators.DataRequired()],choices=[('','Selectionner'),('up','Up'),('down','Down'),('aucun','Pas de Serveur')])
	date_ev= DateField('Date Evenement')
	raison_ev= SelectField('Raison',[validators.DataRequired()])
	date_rap= DateField('Date Rapportage')
	pers_contact= StringField('Personne contactee')
	remarques= StringField('Remarques')
	date_entree= HiddenField('')
	code_utilisateur= HiddenField('')

class FileImportForm(Form):
	fichier= FileField('Fichier')
	type_fichier= SelectField(u'Type Fichier',[validators.DataRequired()],choices=[('','Selectionner'),('Site','Liste Sites'),('Employe','Liste Employes'),('Users','Liste Utilisateurs'),('Evenement','Liste Evenement')])
"""

