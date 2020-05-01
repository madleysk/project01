from django.urls import path
from . import views

urlpatterns = [
	path("",views.index,name="index"),
	path("index",views.index,name="index"),
	path("dashboard/",views.dashboard,name="dashboard"),
	path("subscribe/",views.subscribe,name="subscribe"),
	path("accounts/login/",views.login_view,name="login"),
	path("accounts/logout/",views.logout_view,name="logout"),
	
	path("add_site/",views.add_site,name="add_site"),
	path("edit_site/<int:id_site>",views.edit_site,name="edit_site"),
	path("site/<int:id_site>",views.site,name="site"),
	path("list_sites/",views.list_sites,name="list_sites"),
	path("list_sites/page/<int:page>",views.list_sites,name="list_sites"),
	
	path("add_event/",views.add_event,name="add_event"),
	path("edit_event/<int:id_event>",views.edit_event,name="edit_event"),
	path("list_events/",views.list_events,name="list_events"),
	path("list_events/page/<int:page>",views.list_events,name="list_events"),
]
