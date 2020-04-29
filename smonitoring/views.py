from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import SiteForm
from .models import Site
from .fonctions import import_csv_ev


# Create your views here.
def index(request):
	#return HttpResponse("Hello, world !")
	context= {
		"page_title":"Ma page Accueil",
		"internet_status":{"up":Site.objects.filter(internet="up").count(),"down":Site.objects.filter(internet="down").count()},
		"isante_status":{"up":Site.objects.filter(isante="up").count(),"down":Site.objects.filter(isante="down").count()},
		"fingerprint_status":{"up":Site.objects.filter(fingerprint="up").count(),"down":Site.objects.filter(fingerprint="down").count()},
		"recent_events":Site.objects.order_by('nom')[:5],
		"top_bad_sites":"",
	}
	return render(request, 'dashboard.html', context)

def dashboard(request):
	context= {
		"page_title":"Tableau de bord",
	}
	return render(request, 'dashboard.html', context)

def add_site(request):
	form = SiteForm()
	context= {
		"page_title":"Ajouter Site",
		"form":form,
	}
	#import_csv_ev('smonitoring/uploaded/liste_sites.csv','Site')
	if request.method == 'POST':
		new_site = Site(form)
		new_site.save()
	return render(request, 'site_add.html', context)


def edit_site(request,id_site):
	page_title = 'Modifier site'
	context = {
		"page_title":page_title
	}
	return render(request, 'index.html', context)

def site(request,id_site):
	page_title = 'Information sur le site'
	context = {
		"page_title":page_title
	}
	return render(request, 'index.html', context)

def list_sites(request,page=1):
	"""List of sites with pagination enabled"""
	page_title = 'Liste des sites'
	context = {
		"page_title":page_title
	}
	PER_PAGE = 25
	site_list = Site.objects.all()
	paginator = Paginator(site_list,PER_PAGE)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['liste_sites']=page_obj
	return render(request, 'site_list.html', context)

	
