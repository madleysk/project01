from django.contrib import admin
from smonitoring.models import Site,Evenement

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    """Customize the look of the auto-generated admin for the Member model"""
    #list_display = ('name', 'instrument')
    list_filter = ('nom',)

admin.site.register(Site)  # Use the default options
admin.site.register(Evenement)  # Use the default options
#admin.site.register(Member, MemberAdmin)  # Use the customized options
