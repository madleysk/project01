from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Site, Evenement, RaisonsEvenement, Region, Departement
from datetime import datetime
#from django import Form

EL_STATUS= [('','----------'),('up','Up'),('down','Down'),('none','Non installé')]
LISTE_FAI = [('','----------'),('aucun','N/A'),('digicel','Digicel'),('natcom','Natcom'),('access','Access Haiti'),('hainet','Hainet')]

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=100)
	passwd = forms.CharField(max_length=100, widget=forms.PasswordInput)
	pwd_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput)
	#auth_level = forms.ChoiceField(choices = [('1','User'),('2','Superuser')])
	code = forms.CharField(required=True)
	
	def clean(self):
		super(RegistrationForm, self).clean()
		
		username = self.cleaned_data.get('username')
		passwd = self.cleaned_data.get('passwd')
		pwd_confirm = self.cleaned_data.get('pwd_confirm')
		code = self.cleaned_data.get('code')
		
		if len(username) < 4:
			self._errors['username'] = self.error_class([
			'Nom utilisateur trop court.'
			])
		if passwd != pwd_confirm:
			self._errors['passwd'] = self.error_class([
			'Confirmation mot de passe différente.'
			])
		if len(code) < 4:
			self._errors['code'] = self.error_class([
			'Code invalide.'
			])
		return self.cleaned_data

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	passwd = forms.CharField(max_length=100, widget=forms.PasswordInput)


class SiteForm(forms.Form):
	code = forms.CharField(max_length=100)
	type_site = forms.ChoiceField(choices=[('','----------'),('site','Site'),('bureau','Bureau')])
	nom = forms.CharField(max_length=100)
	sigle = forms.CharField(required=False, max_length=100)
	region = forms.ChoiceField(label='Région')
	departement = forms.ChoiceField(label='Département')
	commune = forms.CharField(required=False, max_length=100)
	adresse = forms.CharField(required=False, max_length=100)
	pepfar = forms.ChoiceField(choices=[('','----------'),('oui','Oui'),('non','Non')])
	contact_1 = forms.CharField(label='Personne de contact 1',max_length=100)
	tel_1 = forms.CharField(label='Numero de téléphone',max_length=100)
	contact_2 = forms.CharField(label='Personne de contact 2',required=False, max_length=100)
	tel_2 = forms.CharField(label='Numero de téléphone',required=False, max_length=100)
	fai = forms.ChoiceField(label='Fournisseur',choices=LISTE_FAI)
	internet = forms.ChoiceField(label='Status Connexion Internet',choices=EL_STATUS)
	isante = forms.ChoiceField(label='Status Serveur isante',choices=EL_STATUS)
	fingerprint = forms.ChoiceField(label='Status Serveur Fingerprint',choices=EL_STATUS)
	
	def clean(self):
		super(SiteForm, self).clean()
		code = self.cleaned_data.get('code')
		
		# Code validation
		if len(code) < 4:
			self._errors['code'] = self.error_class([
			'Code invalide.'
			])
		try:
			code_exists = Site.objects.get(code=code)
			if code_exists is not None:
				self._errors['code'] = self.error_class([
				'Code doit être unique.'
				])
		except Site.DoesNotExist:
			pass

class SiteEditForm(ModelForm):
	class Meta:
		model = Site
		fields = ['code','type_site','nom','sigle','region','departement'\
		,'commune','adresse','pepfar','contact_1','tel_1','contact_2',\
		'tel_2','fai','internet','isante','fingerprint']

class EvenementForm(forms.Form):
	ENTITE_CHOICES = [('','----------'),('internet','Internet'),('isante','Isante Server'),('fingerprint','Fingerprint Server')]
	code_site = forms.ChoiceField(label='Site')
	entite_concerne = forms.ChoiceField(label='Entité concernée',choices=ENTITE_CHOICES) # internet, isante or fingerprint
	status_ev = forms.ChoiceField(label='Status',choices=EL_STATUS) # up, ,down, none
	raison_ev = forms.ChoiceField(label='Raison')
	date_ev = forms.DateField(label='Date événement',widget=forms.SelectDateWidget(), initial=datetime.utcnow)
	date_rap = forms.DateField(label='Date Rapportée',widget=forms.SelectDateWidget(), initial=datetime.utcnow)
	date_entree = forms.CharField(required= False, widget=forms.HiddenInput, initial=datetime.utcnow)
	pers_contact = forms.CharField(required= False,label='Personne de contact',max_length=100)
	remarques = forms.CharField(required= False,max_length=100)
	code_utilisateur = forms.CharField(required= False, widget=forms.HiddenInput)
	"""
	code_site.widget.attrs.update({'class':'form-control'})
	entite_concerne.widget.attrs.update({'class':'form-control'})
	status_ev.widget.attrs.update({'class':'form-control'})
	raison_ev.widget.attrs.update({'class':'form-control'})"""
	def clean(self):
		super(EvenementForm, self).clean()
		date_ev = self.cleaned_data.get('date_ev')
		date_rap = self.cleaned_data.get('date_rap')
		
		if ((date_ev) > (date_rap)):
			self._errors['date_ev'] = self.error_class([
			'Date incohérente.'
			])
		if (date_rap) < (date_ev):
			self._errors['date_rap'] = self.error_class([
			'Date incohérente.'
			])

			
class EvenementEditForm(ModelForm):
	class Meta:
		model = Evenement
		fields = ['code_site','entite_concerne','status_ev','date_ev','raison_ev','date_rap','pers_contact','remarques']
"""	
class EvenementForm(ModelForm):
	class Meta:
		model = Evenement
		fields = ['code_site','entite_concerne','status_ev','date_ev','raison_ev','date_rap','pers_contact','remarques']
"""
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

