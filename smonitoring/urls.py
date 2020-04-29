from django.urls import path
from . import views

urlpatterns = [
	path("",views.index,name="index"),
	path("dashboard",views.dashboard,name="dashboard"),
	path("add_site",views.add_site,name="add_site"),
	path("edit_site/<int:id_site>",views.edit_site,name="edit_site"),
	path("site/<int:id_site>",views.site,name="site"),
	path("list_sites",views.list_sites,name="list_sites"),
	path("list_sites/page/<int:page>",views.list_sites,name="list_sites"),
]
