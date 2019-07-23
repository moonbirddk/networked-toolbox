from django.contrib import admin
from django.utils.html import format_html 
from django.db import models 
from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, Suggestion, ToolFollower, ToolUser, \
    ToolOverviewPage, CategoryOverviewPage, CategoryGroup, CategoryGroupFollower, CategoryGroupOverviewPage, Story, StoryOverviewPage

from django.utils.html import format_html
from trumbowyg.widgets import TrumbowygWidget
from .widgets import ColumnCheckboxSelectMultiple

class EditorAndMultiCheckBoxMixin(admin.ModelAdmin): 
    formfield_overrides = {
        models.TextField: {
            'widget': TrumbowygWidget, 

        }, 
        models.ManyToManyField: {
            'widget': ColumnCheckboxSelectMultiple(
                columns=4, 
                css_class='col-md-4', 
                wrapper_css_class='row',
            ),

            
        }
    }

class ToolAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin): 
    
    def link_to_tool_on_site(self): 
        return format_html('<a href="{}">{}</a>',self.get_absolute_url(), self.title)

    list_per_page = 20 
    list_display = ['title',link_to_tool_on_site,  'created_date', 'published']
    
    
    

class CategoryGroupAdmin(admin.ModelAdmin): 
    list_per_page = 20 
    list_display = ('__str__','published')
    list_editable = ('published',)


class StoryAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin): 

    def link_to_story_on_website(self): 
        url = self.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, str(self))
    
    def tool_or_work_area(self): 
        return '{}: {}'.format(self.parent_object._meta.verbose_name.title(), self.parent_object)
    
    list_display = ['__str__', 'user', tool_or_work_area, link_to_story_on_website, 'created', 'published']
    list_editable = ['published']
    list_select_related = ('user','tool', 'category_group')
    list_per_page = 20
    

class SuggestionAdmin(admin.ModelAdmin): 
    list_display = ['__str__', ]
    list_per_page = 20

class ToolFollowerUserAdmin(admin.ModelAdmin): 
    list_display = ['user', 'tool', 'should_notify']
    list_filter = ['user', 'tool'] #MTODO: Smart Filtering
    list_per_page = 20
    list_select_related = ('tool', 'user')

class CategoryGroupFollowerAdmin(admin.ModelAdmin): 
    lsit_display = ['user','category_group','should_notify']
    list_filter = ['user', 'category_group']
    list_per_page = 20 

class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'group', 'published']
    list_per_page = 20
    list_select_related = ('group',)
    
    
admin.site.register(Tool, ToolAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(ToolFollower, ToolFollowerUserAdmin)
admin.site.register(ToolUser, ToolFollowerUserAdmin)
admin.site.register(CategoryGroupFollower, CategoryGroupFollowerAdmin)
admin.site.register(ToolOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryGroupOverviewPage, SingletonModelAdmin)
admin.site.register(StoryOverviewPage, SingletonModelAdmin)