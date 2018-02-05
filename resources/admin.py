from django.contrib import admin

from .models import ToolResource

class ToolResourceAdmin(admin.ModelAdmin):
	list_display = ['title', 'content_object', 'content_type'] 
	list_per_page = 20

admin.site.register(ToolResource, ToolResourceAdmin)
