from django import template
import bleach
import  html.parser 
register = template.Library()


@register.filter
def bleach_striptags(strval):
    if strval: 
        html_parser = html.parser.HTMLParser()
        output = bleach.clean(strval, tags=[], strip=True, strip_comments=True)
        return html_parser.unescape(output)

@register.inclusion_tag('_svg_icon.html')
def svg_icon(icon_id, *args, **kwargs):
    icon_classes = kwargs.get('icon_classes', '')
    return {
        'icon_id': icon_id,
        'icon_classes': icon_classes,
    }