from django.contrib import admin
from .models import Profile



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

class ProfileAdmin(admin.ModelAdmin): 


	list_display = ['__str__', 'country']
	list_filter= [CountryListFilter,]

admin.site.register(Profile, ProfileAdmin)