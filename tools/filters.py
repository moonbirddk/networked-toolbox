import logging
from itertools import chain
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt, Select
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.html import format_html

import django_filters

from .models import Tool

log = logging.getLogger(__name__)


class BooleanLinksGroupWidget(Select):
    allow_multiple_selected = False

    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        output = [format_html('<div{}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        output.append('</div>')
        return mark_safe('\n'.join(output))

    def render_option(self, name, selected_choices, option_value,
                      option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            query_string = data.urlencode()
        except AttributeError:
            query_string = urlencode(data)
        if selected:
            attrs = ' class="btn btn-danger"'
        else:
            attrs = ' class="btn btn-default"'
        return format_html('<a href="?{}"' + attrs + '>{}</a>',
                           query_string,
                           force_text(option_label))

    def render_options(self, choices, selected_choices, name):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            output.append(self.render_option(name, selected_choices,
                                             option_value, option_label))
        return '\n'.join(output)


class PublishedFilter(django_filters.FilterSet):
    published = django_filters.BooleanFilter(
        label='',
        help_text='',
        name='published',
        widget=BooleanLinksGroupWidget(
            choices=((1, 'published'), (0, 'unpublished')))
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extra = {
        }
        self.filters['published'].extra.update(extra)
