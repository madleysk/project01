from .models import *
from datetime import datetime
import csv
from django import forms
from django.utils import timezone as timezone

def import_csv_ev(fichier,nom_classe):
	with open(fichier) as csv_file:
		csv_reader = csv.reader(csv_file,delimiter=',')
		line_count = 0
		lignes_contenu=[]
		for row in csv_reader:
			if line_count == 0:
				header=", ".join(row).split(",")
				line_count += 1
			else:
				lignes_contenu.append(",".join(row).split(","))
				line_count += 1
		# importing csv file
		if nom_classe == 'Site':
			for site in lignes_contenu:
				print(len(site))
				#Code,type_site,Titre,Commune,Departement,Region,PEPFAR,FAI,internet,isante,fingerprint,Contact_1,Tel,Tel_1,Contact_2,Tel_2
				new_site = Site(code=site[0],type_site=site[1],nom=site[2],sigle='',region=site[5],departement=site[4],commune=site[3],adresse='',pepfar=site[6],contact_1=site[11],tel_1=site[12],contact_2=site[13],tel_2=site[10],fai=site[7],internet=site[8],isante=site[9],fingerprint=site[10])
				new_site.save()
		"""if nom_classe == 'Bureau':
			for bureau in lignes_contenu:
				db.session.add(Bureau(code=bureau[0],pers_resp=bureau[1],fai=bureau[2],adresse=bureau[3],region=bureau[4],departement=bureau[5],tel=bureau[6]))
				db.session.commit()
		if nom_classe == 'Employe':
			for employe in lignes_contenu:
				db.session.add(Employe(code=employe[0],nom=employe[1],prenom=employe[2],email=employe[3],poste=employe[4],adresse=employe[5],tel_perso=employe[6],tel_travail=employe[7],bureau_affecte=employe
				[8]))
			db.session.commit()"""
		if nom_classe == 'Evenement':
			for evenement in lignes_contenu:
				date_entree= timezone.now
				nom_utilisateur= '1001'
				entite_concerne=evenement[2].lower()
				status_ev = evenement[3].lower()
				#date_ev=evenement[4]
				#date_rap=evenement[6]
				site = Site.objects.get(code=evenement[0])
				new_event= Evenement(code_site=site,entite_concerne=entite_concerne.lower(),status_ev=evenement[3].lower(),date_ev=datetime.strptime(evenement[4], '%Y/%M/%d'),raison_ev=evenement[5],date_rap=datetime.strptime(evenement[6], '%Y/%M/%d'),pers_contact=evenement[7],remarques=evenement[8],date_entree=date_entree,nom_utilisateur=nom_utilisateur)
				new_event.save()
				# updating element status
				if entite_concerne.lower() == 'internet':
					site.internet = status_ev
					site.save()
				elif entite_concerne.lower() == 'isante':
					site.isante = status_ev
					site.save()
				elif entite_concerne.lower() == 'fingerprint':
					site.fingerprint = status_ev
					site.save()
				else:
					pass


def import_site_from_csv(fichier):
	lignes = fichier.replace("\r","").split('\n')
	line_count = 0
	new_line_count = 0
	edited_line_count = 0
	for ligne in lignes:
		if line_count == 0:
			header=ligne.split(",")
			line_count += 1
			#print('Entete colonne',header)
		else:
			row=list(ligne.replace('"','').replace("'",'').split(","))
			if len(row) == 17:
				try:
					region = Region.objects.get(code=row[4].upper())
					departement = Departement.objects.get(code=row[5].upper())
					site = Site.objects.get(code=row[0])
					site.code=row[0]
					site.type_site=row[1].lower()
					site.titre=row[2]
					site.sigle=row[3]
					site.region=region
					site.departement=departement
					site.commune=row[6]
					site.adresse=row[7]
					site.pepfar=row[8].lower()
					site.contact_1=row[9]
					site.tel_1=row[10]
					site.contact_2=row[11]
					site.tel_2=row[12]
					site.fai=row[13].lower()
					site.internet=row[14].lower()
					site.isante=row[15].lower()
					site.fingerprint=row[16].lower()
					site.save()
					edited_line_count += 1
				except Site.DoesNotExist:
					new_site = Site(code=row[0],type_site=row[1].lower(),nom=row[2],sigle=row[3],region=region,departement=departement\
					,commune=row[6],adresse=row[7],pepfar=row[8].lower(),contact_1=row[9],tel_1=row[10]\
					,contact_2=row[11],tel_2=row[12],fai=row[13].lower(),internet=row[14].lower(),isante=row[15].lower(),fingerprint=row[16].lower())
					new_site.save()
					new_line_count += 1
				except Region.DoesNotExist:
					pass
				except Departement.DoesNotExist:
					pass
				line_count += 1

	#print(f"{new_line_count} nouvelles lignes, {edited_line_count} modifiees sur un total de {line_count-1} lignes.")
	result= {"new":new_line_count,"edit":edited_line_count,"total":line_count-1}
	return result

def import_event_from_csv(fichier):
	lignes = fichier.replace("\r","").split('\n')
	line_count = 0
	new_line_count = 0
	edited_line_count = 0
	for ligne in lignes:
		if line_count == 0:
			header=ligne.split(",")
			line_count += 1
			#print('Entete colonne',header)
		else:
			ligne= list(ligne.replace('"','').replace("'",'').split(','))
			if len(ligne) > 6 and len(ligne) <= 9:
				code_site= None
				date_entree=timezone.now()
				nom_utilisateur= '1001'
				entite_concerne=''
				status_ev = ''
				site = None
				raison = None
				for evenement in ligne:
					code_site = ligne[0]
					entite_concerne=ligne[2].lower()
					status_ev = ligne[3].lower()
				try:
					raison = RaisonsEvenement.objects.get(desc_ev=ligne[5])
				except RaisonsEvenement.DoesNotExist:
					raison = RaisonsEvenement.objects.get(pk=1)
				try:
					site = Site.objects.get(code=ligne[0])
					new_event= Evenement(code_site=site,entite_concerne=entite_concerne.lower(),status_ev=ligne[3].lower(),date_ev=datetime.strptime(ligne[4], '%Y/%M/%d'),raison_ev=raison,date_rap=datetime.strptime(ligne[6], '%Y/%M/%d'),pers_contact=ligne[7],remarques=ligne[8],date_entree=date_entree,nom_utilisateur=nom_utilisateur)
					new_event.save()
					new_line_count += 1
				except Site.DoesNotExist:
					raise Site.DoesNotExist('Il y a un probleme avec le fichier. Verifier la colonne code site.')

				line_count += 1
				# updating element status
				if entite_concerne.lower() == 'internet':
					site.internet = status_ev
					site.save()
				elif entite_concerne.lower() == 'isante':
					site.isante = status_ev
					site.save()
				elif entite_concerne.lower() == 'fingerprint':
					site.fingerprint = status_ev
					site.save()
				else:
					pass
	result= {"new":new_line_count,"total":line_count-1}
	return result

def format_form_field(form):
	for f in form:
		if not isinstance(f.field.widget, forms.SelectDateWidget):
			f.field.widget.attrs.update({'class':'form-control'})

def pagination_format(page_obj):
	index = page_obj.number
	max_index= len(page_obj.paginator.page_range)
	start_index= index - 3 if index >=3 else 0
	end_index = index + 3 if index <= max_index - 3 else max_index
	page_range = list(page_obj.paginator.page_range)[start_index:end_index]
	return page_range
