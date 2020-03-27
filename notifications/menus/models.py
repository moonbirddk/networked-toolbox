from django.db import models
from django.urls import reverse
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
        blank=True,
        related_name='menu_items', 
        on_delete=models.CASCADE
    )
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=1)

    def get_absolute_url(self):
        if self.page:
            return reverse('pages:show_page', args=(self.page.slug, ))
        elif self.link:
            return self.link
        else:
            return reverse('homepage')
