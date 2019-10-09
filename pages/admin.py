from django.contrib import admin
from .models import Page, FlashText, FooterTextblock, SearchBarInfoText
from tools.admin import EditorAndMultiCheckBoxMixin
from solo.admin import SingletonModelAdmin

class PageAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    fields = ('title', 'slug', 'content', 'published', )

admin.site.register(Page, PageAdmin)
admin.site.register(FlashText, SingletonModelAdmin)
admin.site.register(FooterTextblock, SingletonModelAdmin)
admin.site.register(SearchBarInfoText, SingletonModelAdmin)

