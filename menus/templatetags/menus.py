import os

from django import template
from django.template.loader import get_template, select_template

from menus.models import MenuItem

register = template.Library()

@register.simple_tag
def render_menu(menu):
    """
    Renders the markup for a menu
    """
    labels = [m[1] for m in MenuItem.MENU_CHOICES if m[0]==menu]
    context = {
        'label': labels[0] if len(labels)==1 else 'Unknown menu',
        'items': MenuItem.objects.filter(menu=menu).order_by('order', 'title')
    }
    t = select_template(['menus/menu.html'])
    return t.render(context)
