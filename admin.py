from django.contrib import admin
from smonitoring.models import *

class MyAdminSite(admin.AdminSite):
	site_header = 'Site monitoring Administration'
	index_title = 'Site monitoring Administration'
	site_title = 'Administration Page'

admin_site = MyAdminSite(name='myadmin')

