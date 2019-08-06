
from django.contrib import admin
from django.utils.html import format_html 
from .models import ThreadedComment

class ThreadedCommentAdmin(admin.ModelAdmin): 

	def link_to_related_object(self):
		url = self.related_object.get_absolute_url()
		return format_html('<a href="{}">{}</a>', url, self.related_object.title)

	def related_object_display(self, obj): 
		try: 
			return '{}: {}'.format(
				obj.comment_root.story._meta.model_name.title(), 
				obj.comment_root.story) 
		except: 
			return '{}: {}'.format(
				obj.comment_root.tool._meta.model_name.title(),
				obj.comment_root.tool)
	
	related_object_display.short_description = "Related Object"

	list_display = ['author', 'content_short', link_to_related_object, 'added_dt', 'is_removed']
	list_editable = ['is_removed']
	readonly_fields = ['related_object_display',]
	fields = ['related_object_display', 'author', 'content']
	list_per_page = 20


admin.site.register(ThreadedComment, ThreadedCommentAdmin)

