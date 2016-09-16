from django.db import models

class Page(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.CharField(blank=False, max_length=128)
    content = models.TextField(blank=False)

    def __str__(self):
        return 'Page "%s" (%s)' % (self.page, self.slug)
