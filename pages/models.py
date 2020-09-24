from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe, format_html
from solo.models import SingletonModel  
from adminsortable.models import SortableMixin

class Page(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.CharField(blank=False, max_length=128)
    content = models.TextField(blank=False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return '"%s" (/%s)' % (self.title, self.slug)

    def get_absolute_url(self):
        return reverse('pages:show_page', args=(self.slug, ))

class FlashText(SingletonModel): 
    class Meta: 
        verbose_name = "Old Flash Text"
        
    headline = models.CharField(_('Headline'), max_length=50, null=True, blank=True)
    subtext = models.CharField(_('Subtext'), max_length=200, null=True, blank=True)
    
    def __str__(self):
        return '{} - {}'.format(self.headline, self.subtext)

class FlashTextNew(SortableMixin): 
    class Meta: 
        verbose_name = "Flash Text"
        verbose_name_plural = "Flash Texts"
        ordering = ['order']

    headline = models.CharField(_('Headline'), max_length=50, null=True, blank=True)
    subtext = models.CharField(_('Subtext'), max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True)
    def __str__(self):
        return '{} - {}'.format(self.headline, self.subtext)

class FooterTextblock(SingletonModel): 
    class Meta: 
        verbose_name = _('Footer Contact Text Block')
    headline = models.CharField(_('Headline'), max_length=50, default="Contact the team")
    body = models.TextField(_('Body'), max_length=200,
                            default="To get in touch with the team behind Reflection Action, drop us an e-mail at: ")
    contact_mail = models.EmailField(_('Contact address'), default="reflectionaction@ms.dk")

    def __str__(self): 
        return self.headline

    @property
    def email_link(self): 
        return format_html('mailto:{}', mark_safe(self.contact_mail))

class SearchBarInfoText(SingletonModel): 
    class Meta: 
        verbose_name = _("Search Bar Info Text")

    headline = models.CharField(_('Headline'), max_length=50, default="Looking for a specific tool?")
    body = models.TextField(_('Body'), max_length=200,
                            default="Search within all tools and stories of change here")
    with_highlight = models.BooleanField(_('Use Highlight'), default=True, help_text=_("When checked, the first word of the body texty will be red"))

    def __str__(self): 
        return self.headline
    
    @property
    def body_html(self): 
        span_class = ""
        if self.with_highlight: 
            span_class = "red-text"
        return format_html(
            '<span class="{}">{} </span>{}',
            mark_safe(span_class),  
            mark_safe(self.body.split(' ', 1)[0]), 
            mark_safe(self.body.split(' ', 1)[1])
        )
