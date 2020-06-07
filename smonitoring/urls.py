from django.urls import path
from . import views

urlpatterns = [
	path("",views.index,name="home"),
	path("home",views.index,name="home"),
	path("dashboard/",views.dashboard,name="dashboard"),
	path("accounts/subscribe/",views.subscribe,name="subscribe"),
	path("accounts/login/",views.login_view,name="login"),
	path("accounts/logout/",views.logout_view,name="logout"),
	path("accounts/change_password/",views.change_password,name="change_password"),
	
	path("add_site/",views.add_site,name="add_site"),
	path("import_sites/",views.import_sites,name="import_sites"),
	path("edit_site/<int:id_site>",views.edit_site,name="edit_site"),
	path("view_site/<int:id_site>",views.view_site,name="view_site"),
	path("list_sites/",views.list_sites,name="list_sites"),
	path("list_sites/page/<int:page>",views.list_sites,name="list_sites"),
	
	path("add_event/",views.add_event,name="add_event"),
	path("import_events/",views.import_events,name="import_events"),
	path("edit_event/<int:id_event>",views.edit_event,name="edit_event"),
	path("list_events/",views.list_events,name="list_events"),
	path("list_events/page/<int:page>",views.list_events,name="list_events"),
	
	path("site_stats/<int:id_site>/<str:comp>",views.site_stats,name="site_stats"),
	
	path("internal_api/<str:obj>",views.internal_api,name="api"),
]
