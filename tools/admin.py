from django.contrib import admin

from .models import Tool, ToolCategory, ToolResource, Suggestion

admin.site.register(Tool)
admin.site.register(ToolCategory)
admin.site.register(ToolResource)
admin.site.register(Suggestion)
