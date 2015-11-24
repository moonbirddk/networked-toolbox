import logging
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


log = logging.getLogger(__name__)


class ProfileForm(forms.Form):
    MAX_PHOTO_SIZE = 2 * 1024 * 1024
    PHOTO_MAX_WIDTH = 1024
    PHOTO_MAX_HEIGH = 1024
    first_name = forms.fields.CharField(max_length=30, required=False)
    last_name = forms.fields.CharField(max_length=30, required=False)
    photo = forms.ImageField(required=False,
                             label='Photo image (recommended size: 160x160)')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo and photo.image and photo.file:
            if photo.image.size[0] > self.PHOTO_MAX_WIDTH:
                raise ValidationError("Image width too large ( max %s px )" %
                                      self.PHOTO_MAX_WIDTH)
            if photo.image.size[1] > self.PHOTO_MAX_HEIGH:
                raise ValidationError("Image height too large ( max %s px )" %
                                      self.PHOTO_MAX_HEIGH)
            file_size = len(photo)
            if file_size > self.MAX_PHOTO_SIZE:
                raise ValidationError("Image size is too large ( max %s  )" %
                                      filesizeformat(self.PHOTO_MAX_HEIGH))
            if file_size < 1:
                raise ValidationError("Image is empty" %
                                      filesizeformat(self.PHOTO_MAX_HEIGH))
            return photo
