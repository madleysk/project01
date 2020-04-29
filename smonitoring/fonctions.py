from .models import Site
import csv

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
				site = Site(code=site[0],type_site=site[1],nom=site[2],sigle='',region=site[5],departement=site[4],commune=site[3],adresse='',pepfar=site[6],contact_1=site[11],tel_1=site[12],contact_2=site[13],tel_2=site[10],fai=site[7],internet=site[8],isante=site[9],fingerprint=site[10])
				site.save()
		"""if nom_classe == 'Bureau':
			for bureau in lignes_contenu:
				db.session.add(Bureau(code=bureau[0],pers_resp=bureau[1],fai=bureau[2],adresse=bureau[3],region=bureau[4],departement=bureau[5],tel=bureau[6]))
				db.session.commit()
		if nom_classe == 'Employe':
			for employe in lignes_contenu:
				db.session.add(Employe(code=employe[0],nom=employe[1],prenom=employe[2],email=employe[3],poste=employe[4],adresse=employe[5],tel_perso=employe[6],tel_travail=employe[7],bureau_affecte=employe
				[8]))
			db.session.commit()
		if nom_classe == 'Evenement':
			for evenement in lignes_contenu:
				date_entree= datetime.now().strftime("%Y/%m/%d %H:%M:%S")
				code_utilisateur= current_user.code
				#date_ev=evenement[4]
				#date_rap=evenement[6]
				db.session.add(Evenement(code_site=evenement[0],entite_concerne=evenement[2].lower(),status_ev=evenement[3].lower(),date_ev=evenement[4],raison_ev=evenement[5],date_rap=evenement[6],pers_contact=evenement[7],remarques=evenement[8],date_entree=date_entree,code_utilisateur=code_utilisateur))
			db.session.commit()"""
