import logging
import pytz
from html import escape
from django.conf import settings
from django.utils.timezone import localtime

from profiles.utils import get_profile_photo_url

log = logging.getLogger(__name__)


def format_added_dt(dt, tzstr=settings.TIME_ZONE):
    """
    https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    """
    return localtime(dt, pytz.timezone(tzstr)).strftime('%a %b %y at %H:%m:%S')


def build_comment_data(comment, tzstr=None):
    added_time = format_added_dt(comment.added_dt, tzstr)
    comment_dict = {}
    comment_dict['id'] = comment.id
    comment_dict['parent_id'] = comment.parent_id
    comment_dict['tree_id'] = comment.tree_id
    comment_dict['added_dt'] = comment.added_dt.isoformat()
    comment_dict['added_time'] = escape(added_time, quote=True)
    comment_dict['author_name'] = escape(comment.author.profile.name(),
                                         quote=True)

    comment_dict['author_country_name'] =\
        str(comment.author.profile.country.name)
    comment_dict['author_country_code'] =\
        comment.author.profile.country.code or ''

    comment_dict['author_photo_url'] = get_profile_photo_url(comment.author)
    comment_dict['related_object_id'] = comment.related_object_id
    comment_dict['related_object_type'] = \
        comment.related_object_type.model
    comment_dict['content'] = escape(comment.content, quote=True)
    return comment_dict
