from django.db import models


class Page(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.CharField(blank=False, max_length=128)
    content = models.TextField(blank=False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return '"%s" (/%s)' % (self.title, self.slug)

    def get_absolute_url(self):
        return reverse('pages:show_page', args=(self.slug, ))
