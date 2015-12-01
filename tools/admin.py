from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Tool, ToolCategory, ToolResource, Suggestion, ToolFollower, ToolOverviewPage, CategoryOverviewPage

admin.site.register(Tool)
admin.site.register(ToolCategory)
admin.site.register(ToolResource)
admin.site.register(Suggestion)
admin.site.register(ToolFollower)
admin.site.register(ToolOverviewPage,SingletonModelAdmin)
admin.site.register(CategoryOverviewPage,SingletonModelAdmin)
