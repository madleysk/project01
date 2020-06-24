from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Count, ExpressionWrapper
from .forms import SiteForm, SiteEditForm, EvenementForm,EvenementEditForm, RegistrationForm, ChangePassForm
from .models import Site,Evenement, Region, Departement, RaisonsEvenement
from .fonctions import import_csv_ev,format_form_field, pagination_format,import_site_from_csv,import_event_from_csv
from .MyAccount import MyAccount
import datetime
from django.utils import timezone as timezone
from django.db import connection
from django.db.models import Q # for complex queries
import json
import math
import calendar

PER_PAGE = 25

# Create your views here.
def index(request):
	try:
		filtre = request.GET.get('filter')
	except:
		return HttpResponse('Request problem')
	if filtre != None and filtre != 'all':
		filtre = filtre.upper()
		try:
			filtre = Region.objects.get(nom_region=filtre.capitalize())
		except Region.DoesNotExist:
			filtre = None
		try:
			with connection.cursor() as cursor:
				cursor.execute("SELECT COUNT(*) as qte,code_site_id,nom,nom_region from smonitoring_evenement e, smonitoring_site s, smonitoring_region r WHERE (e.code_site_id=s.id) AND (s.region_id=r.id) AND (e.status_ev=%s) AND (r.nom_region=%s) GROUP BY e.code_site_id,s.nom,r.nom_region ORDER BY qte DESC LIMIT 5",params=['down',filtre.nom_region])
				top_bad_sites = cursor.fetchall()
				top_bad_sites_formated = []
				for t in top_bad_sites:
					top_bad_sites_formated.append({"qte":t[0],"id":t[1],"nom":t[2]})
		except AttributeError:
			raise Http404('No such a region !')

		context= {
			"page_title":"Site Monitoring - Accueil",
			"internet_status":{"up":Site.objects.filter(internet="up",region=filtre).count(),"down":Site.objects.filter(internet="down",region=filtre).count()},
			"isante_status":{"up":Site.objects.filter(isante="up",region=filtre).count(),"down":Site.objects.filter(isante="down",region=filtre).count()},
			"fingerprint_status":{"up":Site.objects.filter(fingerprint="up",region=filtre).count(),"down":Site.objects.filter(fingerprint="down",region=filtre).count()},
			"recent_events":Evenement.objects.select_related('code_site').filter(code_site__region=filtre).order_by('-date_rap')[:5],
			"top_bad_sites":top_bad_sites_formated,
			"filtre":filtre.nom_region.lower(),
			# SELECT COUNT(*) qte,code_site_id,nom from smonitoring_evenement e,smonitoring_site s WHERE e.code_site_id=s.id AND status_ev="down" GROUP BY code_site_id ORDER BY qte DESC LIMIT 5;
		}
		context['internet_total']=round(context['internet_status']['up']*100/Site.objects.filter(region=filtre).exclude(internet__in=['','none']).count(),1)
		context['isante_total']=round(context['isante_status']['up']*100/Site.objects.filter(region=filtre).exclude(isante__in=['','none']).count(),1)
		context['fingerprint_total']=round(context['fingerprint_status']['up']*100/Site.objects.filter(region=filtre).exclude(fingerprint__in=['','none']).count(),1)
		
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
		context['internet_total']=round(context['internet_status']['up']*100/Site.objects.exclude(internet__in=['','none']).count(),1)
		context['isante_total']=round(context['isante_status']['up']*100/Site.objects.exclude(isante__in=['','none']).count(),1)
		context['fingerprint_total']=round(context['fingerprint_status']['up']*100/Site.objects.exclude(fingerprint__in=['','none']).count(),1)
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
			# get url to redirect after login
			nxt = request.GET.get('next')
			if nxt:
				# redirect to the url if defined
				return HttpResponseRedirect(nxt)
			else:
				# else go to home page
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
			username = f1.cleaned_data['username']
			print(username)
			#user.save()			
	else:
		f1 = RegistrationForm(None)
	context['form'] = f1
	return render(request, 'account/subscribe.html', context)

@login_required
def profile(request,update=0):
	if request.method == 'POST':
		acc = MyAccount()
		message=''
		obj_changed=[]
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		if firstname and lastname:
			usr = acc.get_user(request.user.id)
			if usr.first_name != firstname:
				usr.first_name = firstname
				obj_changed.append('Prenoms')
			if usr.last_name != lastname:
				usr.last_name= lastname
				obj_changed.append('Nom')
			if len(obj_changed) == 1:
				usr.save() # save at least one item is different
				message = obj_changed[0] + ' a été changé !'
			elif len(obj_changed) == 2:
				usr.save() # save at least one item is different
				message = obj_changed[0] + ' et '+ obj_changed[1] + ' ont été changés !'
			else:
				message = 'Tout est à jour !'
		else:
			return JsonResponse({"success":True,"message":"Noms et Prenoms sont obligatoires !"})
		# if everything is ok
		return JsonResponse({"success":True,"message":message})
	return JsonResponse({"error":"Argument not submitted"})

@login_required
def change_password(request):
	context= {
		"page_title":"Changer mots de passe",
	}
	if request.method == 'POST':
		f1 = ChangePassForm(request.POST)
		if f1.is_valid():
			username = f1.cleaned_data['username']
			old_passwd = f1.cleaned_data['old_passwd']
			new_pass = f1.cleaned_data['new_pass']
			account = MyAccount()
			usr = account.authenticate(request,username,old_passwd)
			if usr:
				res = account.change_password(request,username,old_passwd,new_pass)
				if res:
					context['msg_success']='Mot de passe changé.'
	else:
		f1 = ChangePassForm(initial={'username':request.user})
	context['form'] = f1
	"""
	if request.method == 'POST':
		username = request.POST.get('username')
		current_pass = request.POST.get('current_pass')
		new_pass = request.POST.get('new_pass')
		new_pass_conf = request.POST.get('new_pass_conf')
		account = MyAccount()
		usr = account.authenticate(request,'admin','MyP')"""
	return render(request, 'account/change_password.html', context)

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
def view_site(request,id_site):
	page_title = 'Information sur le site'
	context = {
		"page_title":page_title
	}
	try:
		id_site = int(id_site)
		site = Site.objects.get(pk=id_site)
		context['page_title']= site.nom
	except Site.DoesNotExist:
		return HttpResponse('Site not exist',404)
		
	int_data_up=[]
	int_data_down=[]
	isante_data_up=[]
	isante_data_down=[]
	fing_data_up=[]
	fing_data_down=[]
	# lambda function to get first day and last day range as a list of two dates
	periode = lambda y,m: [(datetime.date(y,m,1)),(datetime.date(y,m,calendar.monthrange(y,m)[1]))]
	last_year ={
		"months_names":['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sept','Oct','Nov','Déc'],
		"month1":periode((datetime.date.today().year)-1,1),
		"month2":periode((datetime.date.today().year)-1,2),
		"month3":periode((datetime.date.today().year)-1,3),
		"month4":periode((datetime.date.today().year)-1,4),
		"month5":periode((datetime.date.today().year)-1,5),
		"month6":periode((datetime.date.today().year)-1,6),
		"month7":periode((datetime.date.today().year)-1,7),
		"month8":periode((datetime.date.today().year)-1,8),
		"month9":periode((datetime.date.today().year)-1,9),
		"month10":periode((datetime.date.today().year)-1,10),
		"month11":periode((datetime.date.today().year)-1,11),
		"month12":periode((datetime.date.today().year)-1,12),
	}
	q1 = {
		"months_names":['Octobre','Novembre','Décembre'],
		"month1":periode((datetime.date.today().year)-1,10),
		"month2":periode((datetime.date.today().year)-1,11),
		"month3":periode((datetime.date.today().year)-1,12),
	}
	q2 = {
		"months_names":['Janvier','Février','Mars'],
		"month1":periode(datetime.date.today().year,1),
		"month2":periode(datetime.date.today().year,2),
		"month3":periode(datetime.date.today().year,3),
	}
	q3 = {
		"months_names":['Avril','Mai','Juin'],
		"month1":periode(datetime.date.today().year,4),
		"month2":periode(datetime.date.today().year,5),
		"month3":periode(datetime.date.today().year,6),
	}
	q4 = {
		"months_names":['Juillet','Août','Septembre'],
		"month1":periode(datetime.date.today().year,7),
		"month2":periode(datetime.date.today().year,8),
		"month3":periode(datetime.date.today().year,9),
	}
	periodes= {"last_year":last_year,"q1":q1,"q2":q2,"q3":q3,"q4":q4}
	periode= request.GET.get('periode')
	if periode is not None and periode !='last_year':
		event_list = Evenement.objects.filter(code_site=site,date_ev__range=(periodes[periode]['month1'][0],periodes[periode]['month3'][1])).order_by('-date_ev')
		paginator = Paginator(event_list,PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)
		for key,val in periodes[periode].items():
			if key != 'months_names':
				int_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='internet',status_ev='up',date_ev__range=(val[0],val[1])).count())
				int_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='internet',status_ev='down',date_ev__range=(val[0],val[1])).count())
				isante_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='isante',status_ev='up',date_ev__range=(val[0],val[1])).count())
				isante_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='isante',status_ev='down',date_ev__range=(val[0],val[1])).count())
				fing_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='fingerprint',status_ev='up',date_ev__range=(val[0],val[1])).count())
				fing_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='fingerprint',status_ev='down',date_ev__range=(val[0],val[1])).count())
				context['internet_data']=json.dumps({'labels':periodes[periode]['months_names'],'up':{'data':0},'down':{'data':int_data_down}})
				context['isante_data']=json.dumps({'labels':periodes[periode]['months_names'],'up':{'data':0},'down':{'data':isante_data_down}})
				context['fingerprint_data']=json.dumps({'labels':periodes[periode]['months_names'],'up':{'data':0},'down':{'data':fing_data_down}})
		context['periode']= periode
	else:
		event_list = Evenement.objects.filter(code_site=site,date_ev__range=(last_year['month1'][0],last_year['month12'][1])).order_by('-date_ev')
		paginator = Paginator(event_list,PER_PAGE)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj']=page_obj
		context['page_range']= pagination_format(page_obj)
		for key,val in last_year.items():
			if key != 'months_names':
				int_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='internet',status_ev='up',date_ev__range=(val[0],val[1])).count())
				int_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='internet',status_ev='down',date_ev__range=(val[0],val[1])).count())
				isante_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='isante',status_ev='up',date_ev__range=(val[0],val[1])).count())
				isante_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='isante',status_ev='down',date_ev__range=(val[0],val[1])).count())
				fing_data_up.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='fingerprint',status_ev='up',date_ev__range=(val[0],val[1])).count())
				fing_data_down.append(Evenement.objects.select_related('code_site').filter(code_site_id=id_site,entite_concerne='fingerprint',status_ev='down',date_ev__range=(val[0],val[1])).count())

				context['internet_data']=json.dumps({'labels':last_year['months_names'],'up':{'data':0},'down':{'data':int_data_down}})
				context['isante_data']=json.dumps({'labels':last_year['months_names'],'up':{'data':0},'down':{'data':isante_data_down}})
				context['fingerprint_data']=json.dumps({'labels':last_year['months_names'],'up':{'data':0},'down':{'data':fing_data_down}})
		context['periode']= 'last_year'
	
	return render(request, 'site_view.html', context)

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
		new_event.date_entree= timezone.now()
		
			
		if new_event.is_valid():
			code_site=new_event.cleaned_data['code_site']
			entite_concerne=new_event.cleaned_data['entite_concerne']
			status_ev=new_event.cleaned_data['status_ev']
			date_ev= new_event.cleaned_data['date_ev']
			raison_ev= RaisonsEvenement.objects.get(pk= new_event.cleaned_data['raison_ev'])
			date_rap= new_event.cleaned_data['date_rap']
			pers_contact= new_event.cleaned_data['pers_contact']
			remarques= new_event.cleaned_data['remarques']
			date_entree = timezone.now()
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


@login_required
def internal_api(request,obj=None):
	liste=[]
	if obj == 'sites':
		sites = Site.objects.all()
		for site in sites:
			st={
			"id":site.id,
			"code":site.code,
			"nom":site.nom,
			"region":site.region.nom_region,
			"departement":site.departement.nom_departement,
			"internet":site.internet,
			"contact_1":site.contact_1,
			"tel_1":site.tel_1,
			}
			liste.append(st)
	elif obj =='events':
		events = Evenement.objects.all()
		for event in events:
			ev = {
			"id":event.id,
			"evenement":f'{event.entite_concerne} {event.status_ev}',
			"site":f'{event.code_site}',
			"fai":f'{event.code_site.fai}',
			"departement":f'{event.code_site.departement}',
			"region":f'{event.code_site.region}',
			"date_ev":f'{event.date_ev}',
			}
			liste.append(ev)
	return JsonResponse(liste, safe=False)


def site_stats(request, id_site, comp):
	data={}
	if comp == 'internet':
		data= {'labels'  : ['Janvier', 'Fevrier', 'Mars']\
		,'datasets':{'label':'Status Up','backgroundColor':'#008000','borderColor':'#008000'\
		,'hoverBackgroundColor':'#3b8bba','pointBorderColor':'rgba(60,141,188,1)'\
		,'pointHoverBackground':'#fff','pointHoverBorderColor':'rgba(60,141,188,1)'\
		,'fill':'false','data':[3, 1, 2, 0,]}}
		
		return JsonResponse(data)
	
	return JsonResponse(data)
