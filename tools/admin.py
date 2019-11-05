from django.contrib import admin
from django.utils.html import format_html 
from django.db import models 
from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, Suggestion, ToolFollower, ToolUser, \
    ToolOverviewPage, CategoryOverviewPage, CategoryGroup, CategoryGroupFollower, CategoryGroupOverviewPage, Story, StoryOverviewPage

from django.utils.html import format_html
from trumbowyg.widgets import TrumbowygWidget
from .widgets import ColumnCheckboxSelectMultiple

#MTODO FIX ALL ADMIN CHANGE FORMS FOR THEIR NEW LINKS TO 
#COMMENT_ROOT, NOTIFICATION_TARGET, ETC (EXCLUDE_FIELDS MOSTLY) 

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

class OverviewPageAdmnin(EditorAndMultiCheckBoxMixin, SingletonModelAdmin): 
    pass


class FollowerInline(admin.TabularInline):
    fields = ('user',)
    readonly_fields = ('user',)
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args):
        return False


class CategoryGroupFollowerAdmin(admin.ModelAdmin): 
    list_display = ['user','category_group','should_notify']
    list_editable = ['should_notify']
    list_filter = ['user', 'category_group']
    list_per_page = 20 

class CategoryGroupFollowerInline(FollowerInline): 
    model = CategoryGroupFollower


class ToolFollowerUserAdmin(admin.ModelAdmin): 
    list_display = ['user', 'tool', 'should_notify']
    list_editable = ['should_notify']
    list_filter = ['user', 'tool'] #MTODO: Smart Filtering
    list_per_page = 20
    list_select_related = ('tool', 'user')

class ToolFollowerInline(FollowerInline): 
    model = ToolFollower
    
class ToolUserInline(FollowerInline): 
    model = ToolUser

class ToolAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin): 
    
    def link_to_tool_on_site(self): 
        return format_html('<a href="{}">{}</a>',self.get_absolute_url(), self.title)

    list_per_page = 20 
    list_display = ['title',link_to_tool_on_site,  'created_date', 'published']
    inlines = [ToolFollowerInline, ToolUserInline]
    exclude = ['comment_root', 'resource_connection', 'suggestion_root', 'notification_target']

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if inline.get_queryset(request) and inline.get_queryset(request).filter(tool=obj).exists():
                yield inline.get_formset(request, obj), inline
    
    
class CategoryGroupAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    class Meta: 
        model = CategoryGroup

    list_per_page = 20 
    list_display = ('__str__', 'published')
    list_editable = ('published',)
    exclude = ['notification_target']
    inlines = [CategoryGroupFollowerInline, ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if (inline.get_queryset(request) and 
                inline.get_queryset(request).filter(category_group=obj).exists()):
                
                yield inline.get_formset(request, obj), inline

class StoryAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin): 

    def link_to_story_on_website(self): 
        url = self.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, str(self))
    
    def tool_or_work_area(self): 
        return '{}: {}'.format(self.parent_object._meta.verbose_name.title(), self.parent_object)
    
    list_display = ['__str__', 'user', tool_or_work_area, link_to_story_on_website, 'created', 'published']
    list_editable = ['published']
    exclude = ['notification_target', 'comment_root']
    list_select_related = ('user','tool', 'category_group')
    list_per_page = 20
    

class SuggestionAdmin(admin.ModelAdmin): 
    list_display = ['__str__', ] #MTODO FIX THIS 
    list_per_page = 20
    exclude = ['suggestion_root']




class ToolCategoryAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    list_display = ['__str__', 'group', 'published']
    list_per_page = 20
    list_select_related = ('group',)
    exclude = ['resource_connection', 'suggestion_root']
    
    
admin.site.register(Tool, ToolAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
#admin.site.register(ToolFollower, ToolFollowerUserAdmin)
#admin.site.register(ToolUser, ToolFollowerUserAdmin)
#admin.site.register(CategoryGroupFollower, CategoryGroupFollowerAdmin)
admin.site.register(ToolOverviewPage, OverviewPageAdmnin)
admin.site.register(CategoryOverviewPage, OverviewPageAdmnin)
admin.site.register(CategoryGroupOverviewPage, OverviewPageAdmnin)
admin.site.register(StoryOverviewPage, OverviewPageAdmnin)
