from django.contrib import admin
from .models import Page, FlashText
from tools.admin import EditorAndMultiCheckBoxMixin
from solo.admin import SingletonModelAdmin

class PageAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    fields = ('title', 'slug', 'content', 'published', )

admin.site.register(Page, PageAdmin)
admin.site.register(FlashText, SingletonModelAdmin)
