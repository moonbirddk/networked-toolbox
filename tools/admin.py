
from django.contrib import admin
from django.utils.html import format_html 

from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, Suggestion, ToolFollower, \
    ToolOverviewPage, CategoryOverviewPage, CategoryGroup, CategoryGroupOverviewPage, Story


class CategoryGroupAdmin(admin.ModelAdmin): 
	list_per_page = 20 
	list_display = ('__str__','published')
	list_editable = ('published',)

class StoryAdmin(admin.ModelAdmin): 

	def author(self): 
		return self.user
	def link_to_story_on_website(self): 
		url = self.get_absolute_url()
		return format_html('<a href="{}">{}</a>', url, str(self))

	list_display = ['__str__', author, 'tool', link_to_story_on_website, 'created']
	list_per_page = 20

class SuggestionAdmin(admin.ModelAdmin): 
	list_display = ['__str__', 'related_object']
	list_per_page = 20

class ToolFollowerAdmin(admin.ModelAdmin): 
	list_display = ['user', 'tool', 'should_notify']
	list_filter = ['user', 'tool'] #MTODO: Smart Filtering
	list_per_page = 20

class ToolCategoryAdmin(admin.ModelAdmin): 
	list_display = ['__str__', 'group', 'published']
	list_per_page = 20
	
admin.site.register(Tool)
admin.site.register(Story, StoryAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(ToolFollower, ToolFollowerAdmin)
admin.site.register(ToolOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryGroupOverviewPage, SingletonModelAdmin) 