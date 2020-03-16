from django.db import models 
from trumbowyg.widgets import TrumbowygWidget
from django.utils.html import mark_safe
from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin): 
    formfield_overrides = {
        models.TextField: {
            'widget': TrumbowygWidget, 

        }
    }
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    
   
    fields = ['sender', 'headline', 'text', ]
    readonly_fields = ['sender', 'headline', 'text']


admin.site.register(Feedback, FeedbackAdmin)