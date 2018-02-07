from django.contrib import admin
from .models import Page
from tools.admin import EditorAndMultiCheckBoxMixin

class PageAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    fields = ('title', 'slug', 'content', 'published', )

admin.site.register(Page, PageAdmin)
