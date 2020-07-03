from django.contrib import admin

# Register your models here.
from .models import DocumentCategory, LibraryDocument, VideoResource, OnlineCourse, Video, CourseFollower
from filer.admin.fileadmin import FileAdmin

from events_workshops.admin import EventFollowerInline, EventWorkshopAdmin

class CourseFollowerInline(EventFollowerInline): 
    model = CourseFollower

class DocumentAndVideoAdmin(admin.ModelAdmin): 
    exclude = ["comment_root", "notification_target"]

    
class OnlineCourseAdmin(EventWorkshopAdmin): 
    class Meta:
        model = OnlineCourse

    exclude = ["notification_target", "comment_root",]
    inlines = [CourseFollowerInline, ]
    fields = []


admin.site.register(Video)
admin.site.register(VideoResource, DocumentAndVideoAdmin)
admin.site.register(DocumentCategory)
admin.site.register(OnlineCourse, OnlineCourseAdmin)
admin.site.register(LibraryDocument, DocumentAndVideoAdmin)
