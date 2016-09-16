from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(MenuItem, MenuItemAdmin)
