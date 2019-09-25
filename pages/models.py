from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel  

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
    headline = models.CharField(_('Headline'), max_length=50, null=True, blank=True)
    subtext = models.CharField(_('Subtext'), max_length=200, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.headline, self.subtext)
