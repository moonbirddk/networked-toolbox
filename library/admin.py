from django.contrib import admin

# Register your models here.
from .models import DocumentCategory, LibraryDocument, VideoResource, OnlineCourse, Video
from filer.admin.fileadmin import FileAdmin



class DocumentAndVideoAdmin(admin.ModelAdmin): 
    exclude = ["comment_root", ]

    
class OnlineCourseAdmin(admin.ModelAdmin): 
    exclude = ["notification_target", "comment_root", ]

admin.site.register(Video)
admin.site.register(VideoResource, DocumentAndVideoAdmin)
admin.site.register(DocumentCategory)
admin.site.register(OnlineCourse, OnlineCourseAdmin)
admin.site.register(LibraryDocument, DocumentAndVideoAdmin)
