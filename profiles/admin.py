from django.contrib import admin
from .models import Profile
from hijack_admin.admin import HijackRelatedAdminMixin



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

class ProfileAdmin(HijackRelatedAdminMixin, admin.ModelAdmin): 


    list_display = ['__str__', 'country', 'hijack_field']
    list_filter= [CountryListFilter,]
    list_per_page = 20

admin.site.register(Profile, ProfileAdmin)