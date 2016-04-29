
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, Suggestion, ToolFollower, \
    ToolOverviewPage, CategoryOverviewPage, CategoryGroup, Story


admin.site.register(Tool)
admin.site.register(Story)
admin.site.register(ToolCategory)
admin.site.register(CategoryGroup)
admin.site.register(Suggestion)
admin.site.register(ToolFollower)
admin.site.register(ToolOverviewPage, SingletonModelAdmin)
admin.site.register(CategoryOverviewPage, SingletonModelAdmin)
