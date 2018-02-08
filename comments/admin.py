
from django.contrib import admin
from django.utils.html import format_html 
from .models import ThreadedComment

class ThreadedCommentAdmin(admin.ModelAdmin): 

	def link_to_related_object(self):
		url = self.related_object.get_absolute_url()
		return format_html('<a href="{}">{}</a>', url, self.related_object_title)


	list_display = ['author', 'content_short', link_to_related_object, 'added_dt', 'is_removed']
	list_editable = ['is_removed']
	list_per_page = 20


admin.site.register(ThreadedComment, ThreadedCommentAdmin)

