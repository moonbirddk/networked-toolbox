from django.contrib import admin
from django.utils.html import format_html, mark_safe

# Register your models here.
from .models import EventWorkshop, EventFollower

class EventFollowerInline(admin.StackedInline):
    model = EventFollower
    extra = 0
    fields = ('user',)
    readonly_fields = ('user',)

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, *args):
        return False

class  EventWorkshopAdmin(admin.ModelAdmin): 
    class Meta: 
        model = EventWorkshop 
    inlines = [EventFollowerInline, ]
    
    fields = ['event_type', 'title', 'description', 'start_datetime', 'end_datetime', 'participiants']
    readonly_fields = ['participiants']
    
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if inline.get_queryset(request): 
                yield inline.get_formset(request, obj), inline

admin.site.register(EventWorkshop, EventWorkshopAdmin)
