from django.contrib import admin
from smonitoring.models import *
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.

# sites
class SiteAdmin(admin.ModelAdmin):
	list_display = ['code','nom', 'region','fai','internet','pepfar']
	ordering = ['nom']
	actions = ['toggle_internet_status_up','toggle_internet_status_down']
	def toggle_internet_status_up(self, request, queryset):
		updated = queryset.update(internet='up')
		self.message_user(request, ngettext(
			'%d site internet status updated',
			'%d sites internet status updated.',
			updated,
		) % updated, messages.SUCCESS)
	toggle_internet_status_up.allowed_permissions = ('change',)
	def toggle_internet_status_down(self, request, queryset):
		updated = queryset.update(internet='down')
		self.message_user(request, ngettext(
			'%d site internet status updated',
			'%d sites internet status updated.',
			updated,
		) % updated, messages.SUCCESS)
	toggle_internet_status_down.allowed_permissions = ('change',)
    
# evenements
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['date_rap','entite_concerne', 'status_ev','code_site','date_ev']
    ordering = ['-date_rap']
    
#admin.site.register(Site)  # Use the default options
admin.site.register(Site,SiteAdmin)  # Use custum options
#admin.site.register(Evenement)  # Use the default options
admin.site.register(Evenement,EvenementAdmin)  # Use custum options
admin.site.register(Region)  # Use the default options
admin.site.register(Departement)  # Use the default options
admin.site.register(RaisonsEvenement)  # Use the default options

