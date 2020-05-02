from .models import Site,Evenement
from datetime import datetime
import csv
from django import forms

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
				date_entree= datetime.now()
				code_utilisateur= '1001'
				entite_concerne=evenement[2].lower()
				status_ev = evenement[3].lower()
				#date_ev=evenement[4]
				#date_rap=evenement[6]
				site = Site.objects.get(code=evenement[0])
				new_event= Evenement(code_site=site,entite_concerne=entite_concerne.lower(),status_ev=evenement[3].lower(),date_ev=datetime.strptime(evenement[4], '%Y/%M/%d'),raison_ev=evenement[5],date_rap=datetime.strptime(evenement[6], '%Y/%M/%d'),pers_contact=evenement[7],remarques=evenement[8],date_entree=date_entree,code_utilisateur=code_utilisateur)
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
