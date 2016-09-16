from django import forms
from django.forms import fields
from django.utils.text import slugify
from django_summernote.widgets import SummernoteInplaceWidget

class PageForm(forms.Form):
    title = fields.CharField(max_length=128)
    slug = fields.SlugField(max_length=50,
                            required=False,
                            help_text='Leave empty to derive it from the title')
    published = fields.BooleanField(initial=False, required=False)
    content = forms.fields.CharField(
        widget=SummernoteInplaceWidget()
    )

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')
        if not slug and title:
            slug = slugify(title)
        return slug
