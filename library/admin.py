from django.contrib import admin

# Register your models here.
from .models import DocumentCategory, LibraryDocument, VideoResource, OnlineCourse, Video, CourseFollower
from filer.admin.fileadmin import FileAdmin
from events_workshops.admin import EventFollowerInline, EventWorkshopAdmin

class CourseFollowerInline(EventFollowerInline): 
    model = CourseFollower

class VideoAdmin(admin.ModelAdmin): 
    exclude = ["comment_root", "notification_target"]
    list_display = ['__str__', 'category', 'published']
    list_editable = ["published"]

class DocumentAdmin(VideoAdmin): 
    list_dispay = ['title', 'author', 'category', 'published']
    fields = ['author', 'title', 'summary','published','category','document_file','cover_image']

class OnlineCourseAdmin(EventWorkshopAdmin): 
    class Meta:
        model = OnlineCourse

    exclude = ["notification_target", "comment_root",]
    inlines = [CourseFollowerInline, ]
    fields = []
    list_display = ['__str__', 'category', 'start_date_time', 'duration','published']
    list_editable = ["published"]


admin.site.register(VideoResource, VideoAdmin)
admin.site.register(DocumentCategory)
admin.site.register(OnlineCourse, OnlineCourseAdmin)
admin.site.register(LibraryDocument, DocumentAdmin)
