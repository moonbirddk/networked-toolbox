from django.db import models
from django.core.urlresolvers import reverse
from pages.models import Page

class MenuItem(models.Model):
    MENU_FOOTER_LEFT = 'footer-left'
    MENU_FOOTER_CENTER = 'footer-center'
    MENU_FOOTER_RIGHT = 'footer-right'
    MENU_CHOICES = (
        (MENU_FOOTER_LEFT, 'Footer left'),
        (MENU_FOOTER_CENTER, 'Footer center'),
        (MENU_FOOTER_RIGHT, 'Footer right'),
    )
    title = models.CharField(blank=False, max_length=128)
    menu = models.CharField(
        max_length=20,
        choices=MENU_CHOICES,
        default=MENU_FOOTER_LEFT
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
