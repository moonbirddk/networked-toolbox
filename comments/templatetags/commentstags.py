import logging
from collections import OrderedDict
from django import template
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.template import Variable, VariableDoesNotExist, Template
from django.template.loader import get_template, render_to_string
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from bootstrap3.utils import render_tag

from ..models import ThreadedComment
from ..utils import format_added_dt


log = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def format_comment_date(context, dt):
    try:
        return format_added_dt(dt, context['TIMEZONE_NAME'])
    except:
        return ''


@register.simple_tag(takes_context=True)
def render_addcomment_form(context, *args, **kwargs):
    template = get_template('comments/add.html')
    if context is None:
        context = {}
    else: 
        context = context.flatten()
    return template.render(context)


@register.simple_tag
def comments_javascript():
    add_url = reverse('comments:add')
    javascript = """
    <script>
        window.COMMENTS_ADD_COMMENT_URL = '{}';
    </script>
    """.format(add_url)
    url = settings.STATIC_URL + 'js/comments.js'
    commentsjs = render_tag('script', attrs={'src': url})
    javascript = mark_safe(javascript + commentsjs)
    itemjstmpl = get_template('comments/_item_js.html').render({})
    javascript += itemjstmpl
    return javascript


class CommentNode(template.Node):
    """
    Base helper class (abstract) for handling the get_comment_* template tags.
    Looks a bit strange, but the subclasses below should make this a bit more
    obvious.

    based on django comments
    https://github.com/django/django-contrib-comments/blob/master/django_comments/templatetags/comments.py
    """

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_comment_list/count/form and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError(
                "Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError(
                    "Third argument in %r must be 'as'" % tokens[0])
            return cls(
                object_expr=parser.compile_filter(tokens[2]),
                as_varname=tokens[4],
            )

        # {% get_whatever for app.model pk as varname %}
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError(
                    "Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype=CommentNode.lookup_content_type(tokens[2],
                                                          tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3]),
                as_varname=tokens[5]
            )

        else:
            raise template.TemplateSyntaxError(
                "%r tag requires 4 or 5 arguments" % tokens[0])

    @staticmethod
    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get_by_natural_key(app, model)
        except ValueError:
            raise template.TemplateSyntaxError(
                "Third argument in %r must be in the format 'app.model'" %
                tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError(
                "%r tag has non-existant content-type: '%s.%s'" %
                (tagname, app, model))

    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None,
                 as_varname=None, comment=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError(
                "Comment nodes must be given either a literal object or "
                "a ctype and object pk.")
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr
        self.comment = comment

    def render(self, context):
        qs = self.get_queryset(context)
        context[self.as_varname] = self.get_context_value_from_queryset(
            context, qs)
        return ''

    def get_queryset(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return ThreadedComment.objects.none()

        filters = {
            'story': Q(comment_root__story__pk=object_pk),
            'tool': Q(comment_root__tool__pk=object_pk)
        }
        qs = ThreadedComment.objects.select_related('author').filter(
            filters.get(ctype.model)
        ).order_by('tree_id', 'added_dt')
        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
                
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return (
                self.ctype,
                self.object_pk_expr.resolve(context, ignore_failures=True)
            )

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        raise NotImplementedError


class CommentListNode(CommentNode):
    """Insert a list of comments into the context."""

    @classmethod
    def get_comments_dict(cls, qs):
        cdict = OrderedDict({})
        for c in qs:
            if not c.parent_id:
                cdict[c.id] = dict(parent=c, replies=[])
            else:
                cdict[c.parent_id]['replies'].append(c)
        return cdict

    def get_context_value_from_queryset(self, context, qs):
        return CommentListNode.get_comments_dict(qs)


@register.tag
def get_comment_list(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.
    Syntax::
        {% get_comment_list for [object] as [varname]  %}
        {% get_comment_list for [app].[model] [object_id] as [varname]  %}
    Example usage::
        {% get_comment_list for event as comment_list %}
        {% for comment in comment_list %}
            ...
        {% endfor %}
    """
    return CommentListNode.handle_token(parser, token)


class RenderCommentListNode(CommentListNode):
    """Render the comment list directly"""

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_list and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError(
                "Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_list for obj %}
        if len(tokens) == 3:
            object_expr = parser.compile_filter(tokens[2])
            return cls(object_expr=object_expr)

        # {% render_comment_list for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype=CommentNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3])
            )

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "comments/%s/%s/list.html" % (ctype.app_label, ctype.model),
                "comments/%s/list.html" % ctype.app_label,
                "comments/list.html"
            ]
            qs = self.get_queryset(context)
            context_dict = context.flatten()
            context_dict['comment_related_object_type'] = ctype.model
            context_dict['comment_related_object_id'] = object_pk
            context_dict['comment_dict'] = \
                self.get_context_value_from_queryset(context, qs)
            liststr = render_to_string(template_search_list, context_dict)
            return liststr
        else:
            return ''


@register.tag
def render_comment_list(parser, token):
    """
    Render the comment list (as returned by ``{% get_comment_list %}``)
    through the ``comments/list.html`` template
    Syntax::
        {% render_comment_list for [object] %}
        {% render_comment_list for [app].[model] [object_id] %}
    Example usage::
        {% render_comment_list for event %}
    """
    return RenderCommentListNode.handle_token(parser, token)
