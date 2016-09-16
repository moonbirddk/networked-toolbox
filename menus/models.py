from django.db import models
from django.core.urlresolvers import reverse
from pages.models import Page

class MenuItem(models.Model):
    MENU_FOOTER_1 = 'footer-1'
    MENU_FOOTER_2 = 'footer-2'
    MENU_FOOTER_3 = 'footer-3'
    MENU_CHOICES = (
        (MENU_FOOTER_1, 'Networked Toolbox'),
        (MENU_FOOTER_2, 'The Network'),
        (MENU_FOOTER_3, 'The Toolbox'),
    )
    title = models.CharField(blank=False, max_length=128)
    menu = models.CharField(
        max_length=20,
        choices=MENU_CHOICES,
        default=MENU_FOOTER_1
    )
    page = models.ForeignKey(
        Page,
        null=True,
        blank=False,
        related_name='menu_items'
    )
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '"%s" (/%s)' % (self.title, self.slug)
