from django.contrib import admin
from smonitoring.models import *

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    """Customize the look of the auto-generated admin for the Member model"""
    list_filter = ('nom',)

admin.site.register(Site)  # Use the default options
admin.site.register(Evenement)  # Use the default options
admin.site.register(Region)  # Use the default options
admin.site.register(Departement)  # Use the default options
admin.site.register(RaisonsEvenement)  # Use the default options
#admin.site.register(Member, MemberAdmin)  # Use the customized options
