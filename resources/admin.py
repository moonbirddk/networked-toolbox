from django.contrib import admin

from .models import ToolResource

class ToolResourceAdmin(admin.ModelAdmin):

	def related_object_display(self, obj):
		
		try:
			return '{}: {}'.format(
				obj.resource_connection.toolcategory._meta.model_name.title(),
				obj.resource_connection.toolcategory)
		except:
			return '{}: {}'.format(
				obj.resource_connection.tool._meta.model_name.title(),
				obj.resource_connection.tool)

	related_object_display.short_description = "Related Object"

	def related_object_name(self): 
		try:
			return self.resource_connection.toolcategory
		except:
			try: 

				return self.resource_connection.tool
			except:	
				return '-'

	related_object_name.short_description = 'Related Object'


	def related_object_model(self): 
		try:
			return self.resource_connection.toolcategory._meta.verbose_name.title()
		except:
			try: 
				return self.resource_connection.tool._meta.verbose_name.title()
			except: 
				return '-'

	related_object_model.short_description = 'Related Object Type'
			
	readonly_fields = ['related_object_display',]
	fields = ['related_object_display','title', 'document']

	list_display = ['title',related_object_name, related_object_model] 
	list_per_page = 20

admin.site.register(ToolResource, ToolResourceAdmin)
