import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from ..forms import ToolForm

from ..models import Tool, Story, ToolCategory, ToolFollower, ToolUser, ToolOverviewPage, CategoryGroup
from django.contrib.auth.models import User
from comments.models import ThreadedComment
from shared.helpers import OrderedSet
from django.utils.html import format_html
from django.urls import reverse
log = logging.getLogger(__name__)


def list_tools(request):
    ORDERINGS = {
        'a_z': ('alphabetically', 'title'),
        'created': ('recently added', 'created_date'),
        'newest_comments': ('recently discussed', 'comments__added_dt'),
        'most_followed': ('most followed', 'followers'),
        'most_used': ('most used', 'users')
    }
    order_name, order_query = ORDERINGS[request.GET.get('order', 'a_z')]
    queryset = Tool.objects.filter(published=True)
    if 'most' in order_name:
        queryset_ordered=queryset.annotate(num_count=Count(order_query)).order_by('-num_count')

    else:
        queryset_ordered = queryset.order_by(order_query)
    overview = ToolOverviewPage.get_solo()
    category_groups = CategoryGroup.objects.filter(published=True).order_by('name')

    context = {
        'tools_filter': queryset_ordered,
        'category_groups': category_groups,
        'overview': overview,
        'order': order_name,
        'order_by_list': ORDERINGS,
    }
    return render(request, 'tools/index.html', context)


def show_tool(request, tool_id):
    if request.user.has_perm('tools.change_tool'):
        tool = get_object_or_404(Tool, id=tool_id)
    else:
        tool = get_object_or_404(Tool, id=tool_id, published=True)
    comments = tool.comments.all()
    tool_follower_ids = list(tool.followers.all().values_list('user_id', flat=True))
    tool_followers = tool.followers.all().order_by('?')[:12]
    tool_users = tool.users.all().order_by('?')[:12]
    tool_user_ids = list(tool.users.all().values_list('user_id', flat=True))
    stories = tool.stories.all().order_by('-created')
    tools_home_objects = {
        'st': Story, 
        'tb': ToolCategory
    }
    parent_object = None
    parent_id = None
    if "_" in request.GET.get('from'): 
        parent_object, parent_id = request.GET.get('from').split('_')
        parent_object_instance = tools_home_objects.get(parent_object).objects.get(id=parent_id)
    if parent_object: 
        tools_home = format_html('<a href="{}">{}</a>', parent_object_instance.get_absolute_url(), parent_object_instance)    
    else: 
        tools_home = format_html('<a href="{}">Tools</a>', reverse('tools:list_tools'))
    
    breadcrumbs = [
        tools_home, 
        tool.title
    ]
    context = {
        'breadcrumbs': breadcrumbs,
        'meta': tool._meta, 
        'tool': tool,
        'tool_follower_ids': tool_follower_ids,
        'tool_followers': tool_followers,
        'tool_users': tool_users, 
        'tool_user_ids': tool_user_ids,  
        'stories': stories,
        'comments': comments
    }

    return render(request, 'tools/show.html', context)


@transaction.atomic
@login_required
def follow_tool(request, tool_id):

    tool = get_object_or_404(Tool, id=tool_id, published=True)
    if request.method == 'POST':
        nessage = ''
        should_notify = False
        if request.POST.get('should_notify', '0') == '1':
            should_notify = True
            ToolFollowerOrUser = ToolFollower
            message = 'You are now following this tool.'
        elif request.POST.get('have_used', '0') == '1': 
            ToolFollowerOrUser = ToolUser
            message = 'You have used this tool.'   
        tool_follower, created = ToolFollowerOrUser.objects.get_or_create(
        user=request.user,
        tool=tool
        )
        tool_follower.should_notify = should_notify
        messages.success(request, message)    
    return redirect(tool)


@login_required
def unfollow_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id, published=True)
    if request.method == 'POST':
        if request.POST.get('have_used'):
            tool_followers_or_users = tool.users.all()
            message = "You have not used this tool."
        elif request.POST.get('should_notify'): 
            tool_followers_or_users = tool.followers.all()
            message = "You are no longer following this tool."
        tool_followers_or_users.filter(user_id=request.user.id).delete()
        messages.success(request, message)
    return redirect(tool)



