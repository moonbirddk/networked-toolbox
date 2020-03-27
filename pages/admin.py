from django.contrib import admin
from .models import Page, FlashText, FlashTextNew, FooterTextblock, SearchBarInfoText
from tools.admin import EditorAndMultiCheckBoxMixin
from solo.admin import SingletonModelAdmin
from adminsortable.admin import SortableAdmin

class PageAdmin(EditorAndMultiCheckBoxMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    fields = ('title', 'slug', 'content', 'published', )

class FlashTextAdmin(admin.ModelAdmin): 
    pass

admin.site.register(Page, PageAdmin)
admin.site.register(FlashTextNew, SortableAdmin)
#admin.site.register(FlashText, SingletonModelAdmin)
admin.site.register(FooterTextblock, SingletonModelAdmin)
admin.site.register(SearchBarInfoText, SingletonModelAdmin)

