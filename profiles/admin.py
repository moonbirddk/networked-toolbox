from django.contrib import admin
from django.urls import path
from .models import Profile
from hijack_admin.admin import HijackRelatedAdminMixin
from allauth.account.models import EmailAddress
from allauth.account.admin import EmailAddressAdmin
from import_export.admin import ExportMixin
from import_export.formats.base_formats import CSV, XLS, XLSX

class CountryListFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        countries = set([t.country for t in model_admin.model.objects.all()])    
        return [(country, country.name)for country in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country=self.value())
        else:
            return queryset

class EmailAddressAdminCustom(ExportMixin, EmailAddressAdmin):
    formats = [CSV, XLS, XLSX]
    

class ProfileAdmin(HijackRelatedAdminMixin, admin.ModelAdmin): 


    list_display = ['__str__', 'country', 'hijack_field']
    list_filter= [CountryListFilter,]
    list_per_page = 20


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdminCustom)
