from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import humanize
import datetime

from comments.models import CommentRoot

#from shared.db.fields import FilerVideoField

#from shared.db.fields import 
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from filer.models.filemodels import File
from filer import settings as filer_settings

import os 

# Create your models here.
 
### model for VideoFileField
class Video(File):
    @classmethod 
    def matches_file_type(cls, iname, ifile, request): 
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv', ]
        extension = os.path.splitext(iname)[1].lower()
        return extension in filename_extensions

    _icon = "video"


class FilerVideoField(FilerFileField):
    udefault_model_class = Video



class DocumentCategory(models.Model): 
    class Meta: 
        verbose_name = "Document Category"
        verbose_name_plural = "Document Categories"

    name = models.CharField(_('Category Name'), max_length=75)
    created = models.DateTimeField(_("Created Date"), auto_now_add=True)

    def __str__(self): 
        return self.name


class LibraryResource(models.Model): 
    class Meta: 
        abstract = True

    title = models.CharField(_("Title"), max_length=255, help_text=_("Enter Document Title here."), null=True)
    summary = models.TextField(_("Short Summary"), max_length=1000, help_text=_("Enter a short summary (max. 1000 characters)"), null=True)
    upload_date = models.DateTimeField(_('Upload Date'), auto_now_add=True, null=True)
    published = models.BooleanField(_("Published"), default=False)
    comment_root = models.OneToOneField("comments.CommentRoot", on_delete=models.CASCADE, null=True)

    @property
    def document_class(self): 
        return self._meta.verbose_name

    def get_absolute_url(self):

        return reverse('library:show_{}'.format(self._meta.model_name), args=(self.id, ))

    @property
    def comments(self):
        if self.comment_root is not None: 
            return self.comment_root.comments.all()
        

    def __str__(self):
        return self.title


class VideoResource(LibraryResource): 
    class Meta: 
        verbose_name = "Video Resource"
        verbose_name_plural = "Video Resources"

    video_file = FilerVideoField(verbose_name=_("Video file"), related_name="video_resource", on_delete=models.CASCADE)
    category = models.ForeignKey('library.DocumentCategory', verbose_name=_(
        "Document Category"), on_delete=models.CASCADE, related_name="videos", null=True)
    
class OnlineCourse(LibraryResource): 
    class Meta: 
        verbose_name = "Online Course"
        verbose_name_plural = "Online Courses"
    
    cover_image = FilerImageField(verbose_name=_(
        'Cover Image'), related_name="course_cover_image", null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey("library.DocumentCategory", verbose_name=_("Document Category"), related_name="courses", on_delete=models.CASCADE, null=True)
    start_date_time = models.DateTimeField(_("Start Date And Time"))
    end_date_time = models.DateTimeField(_("End Date And Time"))
    notification_target = models.OneToOneField(
        'user_notifications.NotificationTarget', on_delete=models.CASCADE, null=True)

    @property
    def duration(self):
        return humanize.naturaldelta(self.end_date_time - self.start_date_time)




class LibraryDocument(LibraryResource): 
    class Meta: 
        verbose_name = "Library Document"
        verbose_name_plural = "Library Documents"

    category = models.ForeignKey('library.DocumentCategory', verbose_name=_(
        "Document Category"), on_delete=models.CASCADE, related_name="documents")
    document_file = FilerFileField(verbose_name=_(
        'Library Document'), related_name="library_document", on_delete=models.CASCADE,)
    cover_image = FilerImageField(verbose_name=_(
        'Cover Image'), related_name="document_cover_image", null=True, blank=True, on_delete=models.CASCADE)

@receiver(post_save, sender=LibraryDocument)
def document_saved(sender, instance, created, **kwargs):
    import pdb; pdb.set_trace()
    if created:
        comment_root = CommentRoot()
        comment_root.save()
        instance.comment_root = comment_root
        instance.save()
