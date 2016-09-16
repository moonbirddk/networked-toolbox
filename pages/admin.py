from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    fields = ('title', 'slug', 'content', 'published', )

admin.site.register(Page, PageAdmin)
