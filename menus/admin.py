from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'order', 'page', 'link']
    ordering = ('menu', 'order', 'title')

admin.site.register(MenuItem, MenuItemAdmin)
