from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Count, ExpressionWrapper
from .forms import SiteForm, SiteEditForm, EvenementForm,EvenementEditForm, RegistrationForm
from .models import Site,Evenement, Region, Departement, RaisonsEvenement
from .fonctions import import_csv_ev,format_form_field, pagination_format,import_site_from_csv,import_event_from_csv
from datetime import datetime
from django.db import connection
from django.db.models import Q # for complex queries

PER_PAGE = 25

# Create your views here.
def index(request):
	try:
		filtre = request.GET.get('filter')
	except:
		return HttpResponse('Request problem')
	if filtre != None and filtre != 'all':
		filtre = filtre.upper()
		with connection.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) as qte,code_site_id,nom from smonitoring_evenement e, smonitoring_site s WHERE (e.code_site_id=s.id) AND (e.status_ev=%s) AND (s.region=%s) GROUP BY e.code_site_id,s.nom ORDER BY qte DESC LIMIT 5", params=['down',filtre.upper()])
			top_bad_sites = cursor.fetchall()
			top_bad_sites_formated = []
			for t in top_bad_sites:
				top_bad_sites_formated.append({"qte":t[0],"id":t[1],"nom":t[2]})
		context= {
			"page_title":"Site Monitoring - Accueil",
			"internet_status":{"up":Site.objects.filter(internet="up",region=filtre).count(),"down":Site.objects.filter(internet="down",region=filtre).count()},
			"isante_status":{"up":Site.objects.filter(isante="up",region=filtre).count(),"down":Site.objects.filter(isante="down",region=filtre).count()},
			"fingerprint_status":{"up":Site.objects.filter(fingerprint="up",region=filtre).count(),"down":Site.objects.filter(fingerprint="down",region=filtre).count()},
			"recent_events":Evenement.objects.select_related('code_site').filter(code_site__region=filtre).order_by('-date_rap')[:5],
			"top_bad_sites":top_bad_sites_formated,
			"filtre":filtre.lower(),
			# SELECT COUNT(*) qte,code_site_id,nom from smonitoring_evenement e,smonitoring_site s WHERE e.code_site_id=s.id AND status_ev="down" GROUP BY code_site_id ORDER BY qte DESC LIMIT 5;
		}
		#print(context['recent_events'].query)
		
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) as qte,code_site_id,nom from smonitoring_evenement e,smonitoring_site s WHERE e.code_site_id=s.id AND e.status_ev=%s GROUP BY code_site_id,s.nom ORDER BY qte DESC LIMIT 5",params=['down'])
			top_bad_sites = cursor.fetchall()
			top_bad_sites_formated = []
			for t in top_bad_sites:
				top_bad_sites_formated.append({"qte":t[0],"id":t[1],"nom":t[2]})
		context= {
			"page_title":"Site Monitoring - Accueil",
			"internet_status":{"up":Site.objects.filter(internet="up").count(),"down":Site.objects.filter(internet="down").count()},
			"isante_status":{"up":Site.objects.filter(isante="up").count(),"down":Site.objects.filter(isante="down").count()},
			"fingerprint_status":{"up":Site.objects.filter(fingerprint="up").count(),"down":Site.objects.filter(fingerprint="down").count()},
			"recent_events":Evenement.objects.order_by('-date_rap').select_related('code_site')[:5],
			"top_bad_sites":top_bad_sites_formated,
			# SELECT COUNT(*) qte,code_site_id,nom from smonitoring_evenement e,smonitoring_site s WHERE e.code_site_id=s.id AND status_ev="down" GROUP BY code_site_id ORDER BY qte DESC LIMIT 5;
		}
	return render(request, 'dashboard.html', context)

def dashboard(request):
	context= {
		"page_title":"Site Monitoring - Tableau de bord",
		"internet_status":{"up":Site.objects.filter(internet="up").count(),"down":Site.objects.filter(internet="down").count()},
		"isante_status":{"up":Site.objects.filter(isante="up").count(),"down":Site.objects.filter(isante="down").count()},
		"fingerprint_status":{"up":Site.objects.filter(fingerprint="up").count(),"down":Site.objects.filter(fingerprint="down").count()},
		"recent_events":Evenement.objects.order_by('date_rap').select_related('code_site')[:5],
		"top_bad_sites":Evenement.objects.filter(status_ev='down').select_related('code_site')[:5],
	}

	return render(request, 'dashboard.html', context)

def login_view(request):
	context= {
		"page_title":"Connexion",
	}
	if request.method == 'POST':
		username = request.POST["username"]
		passwd = request.POST["passwd"]
		user = authenticate(request,  username=username, password=passwd)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("home"))
		else:
			context['errors']= 'Erreur de mot de passe ou nom utilisateur.'
	return render(request, 'login.html', context)
	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("login"))
	
def subscribe(request):
	context= {
		"page_title":"Inscription",
	}
	
	form = RegistrationForm()
	
	if request.method == 'POST':
		f1 = RegistrationForm(request.POST)
		if f1.is_valid():
			user = f1.save(commit = False)
			#user.save()			
	else:
		f1 = RegistrationForm(None)
	context['form'] = f1
	return render(request, 'subscribe.html', context)

@login_required
def add_site(request):
	LISTE_REGIONS= [('','----------')] +[(r.id,r.nom_region) for r in Region.objects.all().order_by('nom_region')]
	LISTE_DEPTS= [('','----------')] +[(d.id,d.nom_departement) for d in Departement.objects.all().order_by('nom_departement')]
	context= {
		"page_title":"Ajouter Site",
	}
	#import_csv_ev('smonitoring/uploaded/liste_sites.csv','Site')
	if request.method == 'POST':
		form = SiteForm(request.POST)
		form.fields['region'].choices = LISTE_REGIONS
		form.fields['departement'].choices = LISTE_DEPTS
		format_form_field(form)
		
		if form.is_valid():
			vals=[]
			# get form submitted values and add them to the list
			for field in form.cleaned_data:
				vals.append(form.cleaned_data[field])
			# Getting the necessary instances
			region = Region.objects.get(pk=vals[4])
			dept = Departement.objects.get(pk=vals[5])
			# Creating new site object and save it to the database
			new_site = Site(code=vals[0],type_site=vals[1],nom=vals[2]\
			,sigle=vals[3],region=region,departement=dept,commune=vals[6]\
			,adresse=vals[7],pepfar=vals[8],contact_1=vals[9],tel_1=vals[10],contact_2=vals[11]\
			,tel_2=vals[12],fai=vals[13],internet=vals[15],isante=vals[15],fingerprint=vals[16])
			new_site.save()	
			# redirect to the sites list page	
			return HttpResponseRedirect(reverse('list_sites'))
	else:
		form = SiteForm(None)
		form.fields['region'].choices = LISTE_REGIONS
		form.fields['departement'].choices = LISTE_DEPTS
		format_form_field(form)
	
	context['form']=form
	return render(request, 'site_add.html', context)

@login_required
def edit_site(request,id_site):
	context = {
		"page_title": 'Modifier site'
	}
	try:
		site= Site.objects.get(pk=id_site)
	except Site.DoesNotExist:
		return HttpResponseRedirect(reverse('list_sites'))
	if request.method == 'POST':
		form = SiteEditForm(request.POST,instance=site)
		format_form_field(form)
		if form.is_valid():
			site_edited = form.save()
			return HttpResponseRedirect(reverse('list_sites'))
	else:
		form = SiteEditForm(instance=site)
		format_form_field(form)
	context['form']= form
	return render(request, 'site_edit.html', context)

@login_required
def site(request,id_site):
	page_title = 'Information sur le site'
	context = {
		"page_title":page_title
	}
	return render(request, 'index.html', context)

@login_required
def list_sites(request,page=1):
	"""List of sites with pagination enabled"""
	page_title = 'Liste des sites'
	context = {
		"page_title":page_title,
	}
	keyword= request.GET.get('search')
	if keyword is not None:
		# searching for the keywords
		site_list = Site.objects.filter(Q(nom__icontains=keyword) | Q(code__icontains=keyword)).order_by('nom')
		paginator = Paginator(site_list,PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)
	else:
		site_list = Site.objects.all().order_by('nom')
		paginator = Paginator(site_list,PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)
	msg= request.GET.get('msg')

	return render(request, 'site_list.html', context)

@login_required
def import_sites(request):
	"""Import sites from csv file"""
	page_title = 'Importer des sites'
	context = {
		"page_title":page_title,
		"info":"Code*, type_site*, Titre*, sigle, Region*, Departement*, Commune*, Adresse, PEPFAR, Contact_1*, Tel_1*, Contact_2, Tel, FAI, internet, isante, fingerprint",
	}

	if request.method == 'POST':
		# import commands
		try:
			csv_file = request.FILES['fichier']
		except:
			return HttpResponse('Something when wrong')
		if csv_file is not None:
			if csv_file.name.endswith('.csv'):
				if csv_file.multiple_chunks() is False:
					try:
						file_data = csv_file.read().decode("utf-8")
						result = import_site_from_csv(file_data)
						context['msg_success']= f'{result["new"]} ligne(s) inserée(s), {result["edit"]} modifiée(s) sur {result["total"]} ligne(s).'
						return render(request, 'file_import.html', context)
					except UnicodeDecodeError:
						context['msg_error']= 'Erreur de decodage de fichier.' 
						context['msg_info']= 'Veuillez convertir le fichier en utf-8.' 
						return render(request, 'file_import.html', context)
					except:
						context['msg_error']= 'Erreur inconnue.' 
						return render(request, 'file_import.html', context)
				else:
					context['msg_error']= 'Fichier trop lourd !.' 
					return render(request, 'file_import.html', context)
			else:
				context['msg_error']= 'Type de fichier non permis.' 
				context['msg_info']= 'Seulement les fichiers csv sont permis.' 
				return render(request, 'file_import.html', context)
	return render(request, 'file_import.html', context)

@login_required
def add_event(request):
	context= {
		"page_title":"Ajouter Evénement",
	}
	#import_csv_ev('smonitoring/uploaded/complete_event_list.csv','Evenement')
	LISTE_SITES=[('','----------')]+[(s.id,s.nom) for s in Site.objects.order_by('nom').all()]
	RAISON_CHOICES= [('','----------')] +[(r.id,r.desc_ev) for r in RaisonsEvenement.objects.all().order_by('desc_ev')]
	if request.method == 'POST':
		new_event = form = EvenementForm(request.POST)
		new_event.fields['code_site'].choices = LISTE_SITES
		new_event.fields['raison_ev'].choices = RAISON_CHOICES
		new_event.date_entree=timezone.now
		
			
		if new_event.is_valid():
			code_site=new_event.cleaned_data['code_site']
			entite_concerne=new_event.cleaned_data['entite_concerne']
			status_ev=new_event.cleaned_data['status_ev']
			date_ev= new_event.cleaned_data['date_ev']
			raison_ev= RaisonsEvenement.objects.get(pk= new_event.cleaned_data['raison_ev'])
			date_rap= new_event.cleaned_data['date_rap']
			pers_contact= new_event.cleaned_data['pers_contact']
			remarques= new_event.cleaned_data['remarques']
			date_entree = timezone.now
			nom_utilisateur = '1001'
			site = Site.objects.get(pk=code_site)
			new_event = Evenement(code_site=site,entite_concerne=entite_concerne,status_ev=status_ev\
			,date_ev=date_ev,raison_ev=raison_ev,date_rap=date_rap,date_entree=date_entree,pers_contact=pers_contact\
			,remarques=remarques,nom_utilisateur=nom_utilisateur)
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
			if request.POST.get('serveurs'):
				isante_status = request.POST.get('isante_status')
				raison_isante = request.POST.get('raison_isante')
				fingerprint_status = request.POST.get('fingerprint_status')
				raison_fingerprint = request.POST.get('raison_fingerprint')
				if isante_status:
					new_event = Evenement(code_site=site,entite_concerne='isante',status_ev=isante_status\
					,date_ev=date_ev,raison_ev=raison_isante,date_rap=date_rap,date_entree=date_entree,pers_contact=pers_contact\
					,remarques=remarques,nom_utilisateur=nom_utilisateur)
					new_event.save()
					site.isante = isante_status
					site.save()
				if fingerprint_status:
					new_event = Evenement(code_site=site,entite_concerne='fingerprint',status_ev=fingerprint_status\
					,date_ev=date_ev,raison_ev=raison_fingerprint,date_rap=date_rap,date_entree=date_entree,pers_contact=pers_contact\
					,remarques=remarques,nom_utilisateur=nom_utilisateur)
					new_event.save()
					site.fingerprint = fingerprint_status
					site.save()
					
			return HttpResponseRedirect(reverse("list_events"))
	else:
		form = EvenementForm(None)
		form.fields['code_site'].choices = LISTE_SITES
		form.fields['raison_ev'].choices = RAISON_CHOICES
		format_form_field(form)

	context['form'] = form
	return render(request, 'event_add.html', context)

@login_required
def edit_event(request,id_event):
	"""List of sites with pagination enabled"""
	page_title = 'Modification Evénements'
	event= Evenement.objects.get(pk=id_event)
	context = {
		"page_title":page_title
	}
	if request.method == 'POST':
		form = EvenementEditForm(request.POST,instance=event)
		format_form_field(form)
		if form.is_valid():
			event_edited = form.save()
			return HttpResponseRedirect(reverse('list_events'))
	else:
		form = EvenementEditForm(instance=event)
		format_form_field(form)
	context['form']= form
	return render(request, 'event_edit.html', context)

@login_required
def list_events(request,page=1):
	"""List of sites with pagination enabled"""
	page_title = 'Liste des Evénements'
	context = {
		"page_title":page_title
	}
	keyword= request.GET.get('search')
	if keyword is not None:
		event_list = Evenement.objects.select_related('code_site')\
		.filter(Q(code_site__nom__icontains=keyword) | Q(entite_concerne__icontains=keyword)).order_by('-date_entree')
		paginator = Paginator(event_list, PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)
		context['url_params'] = '&search='+keyword
	else:
		event_list = Evenement.objects.all().select_related('code_site').order_by('-date_entree')
		paginator = Paginator(event_list, PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)

	return render(request, 'event_list.html', context)
		
@login_required
def import_events(request):
	"""Import events from csv file"""
	context= {
		"page_title":'Importer des Evénements',
		"info_title":'Importer des Evénements',
		"info":"code_site*, Nom du site*, Evènement*, status_ev*, date_ev*, raison, date_rap*, pers_cont, Autres remarques.",
	}
	
	if request.method == 'POST':
		# import commands
		try:
			csv_file = request.FILES['fichier']
		except:
			return HttpResponse('Something when wrong')
		if csv_file is not None:
			if csv_file.name.endswith('.csv'):
				if csv_file.multiple_chunks() is False:
					try:
						file_data = csv_file.read().decode("utf-8")
						result = import_event_from_csv(file_data)
						context['msg_success']= f'{result["new"]} ligne(s) inserée(s) sur {result["total"]} ligne(s).' 
						return render(request, 'file_import.html', context)
					except UnicodeDecodeError:
						context['msg_error']= 'Erreur de decodage de fichier.' 
						context['msg_info']= 'Veuillez convertir le fichier en utf-8.' 
						return render(request, 'file_import.html', context)
					except:
						context['msg_error']= 'Erreur inconnue.' 
						return render(request, 'file_import.html', context)
				else:
					context['msg_error']= 'Fichier trop lourd !.' 
					return render(request, 'file_import.html', context)
			else:
				context['msg_error']= 'Type de fichier non permis.' 
				context['msg_info']= 'Seulement les fichiers csv sont permis.' 
				return render(request, 'file_import.html', context)
	return render(request, 'file_import.html', context)

