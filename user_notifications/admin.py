# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import UserNotification


class UserNotificationAdmin(admin.ModelAdmin):
    
    raw_id_fields = ('recipient',)
    list_display = ('recipient', 'actor',
                    'level', 'target', 'unread', 'public')
    list_filter = ('level', 'unread', 'public', 'timestamp',)

    def target_display(self):
        return self.target

    readonly_fields = [target_display,]
    fields = [
        'level',
        'recipient',
        'actor',
        'verb',
        target_display,
        'description',
        'timestamp',
        'unread',
        'public',
        'deleted',
        'emailed',
        'data'
    ]
admin.site.register(UserNotification, UserNotificationAdmin)
