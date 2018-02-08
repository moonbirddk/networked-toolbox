import bleach
from django import template
import  html.parser 
register = template.Library()


@register.filter
def bleach_striptags(strval):
    if strval: 
        html_parser = html.parser.HTMLParser()
        output = bleach.clean(strval, tags=[], strip=True, strip_comments=True)
        return html_parser.unescape(output)
