
from django.contrib import admin
from django.utils.html import format_html 

from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, Suggestion, ToolFollower, \
    ToolOverviewPage, CategoryOverviewPage, CategoryGroup, Story



class StoryAdmin(admin.ModelAdmin): 

	def author(self): 
		return self.user
	def link_to_story_on_website(self): 
		url = self.get_absolute_url()
		return format_html('<a href="{}">{}</a>', url, str(self))

	list_display = ['__str__', author, 'tool', link_to_story_on_website, 'created']

class SuggestionAdmin(admin.ModelAdmin): 
	list_display = ['__str__', 'related_object']

class ToolFollowerAdmin(admin.ModelAdmin): 
	list_display = ['user', 'tool', 'should_notify']
	list_filter = ['user', 'tool'] #MTODO: Smart Filtering

class ToolCategoryAdmin(admin.ModelAdmin): 
	list_display = ['__str__', 'group', 'published']

admin.site.register(Tool)
admin.site.register(Story, StoryAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(CategoryGroup)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(ToolFollower, ToolFollowerAdmin)
admin.site.register(ToolOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryOverviewPage, SingletonModelAdmin)
