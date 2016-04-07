import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, permission_required

from ..filters import PublishedFilter
from ..forms import ToolForm

from ..models import Tool, ToolCategory, ToolFollower, ToolOverviewPage
from django.contrib.auth.models import User


log = logging.getLogger(__name__)


@transaction.atomic
@permission_required('tools.add_tool', login_url='tools:index')
@login_required
def add(request):
    form = ToolForm()

    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            categories = form.cleaned_data.get('categories', [])
            del form.cleaned_data['categories']
            tool = Tool.objects.create(**form.cleaned_data)
            tool.save()
            tool.categories = categories
            messages.success(request, "You created a tool")
            return redirect(tool)

    context = {'form': form}
    return render(request, 'tools/add.html', context)


def index(request):
    if request.user.has_perm('tools.change_tool'):
        queryset = Tool.objects.all().order_by('-published')
    else:
        queryset = Tool.objects.filter(published=True)
    tools_filter = PublishedFilter(request.GET, queryset=queryset)
    overview = ToolOverviewPage.get_solo()
    context = {'tools_filter': tools_filter, 'overview': overview}
    return render(request, 'tools/index.html', context)


def show(request, tool_id):
    if request.user.has_perm('tools.change_tool'):
        tool = get_object_or_404(Tool, id=tool_id)
    else:
        tool = get_object_or_404(Tool, id=tool_id, published=True)

    tool_followers = (list(tool.followers.all().values_list('user_id', flat=True)))
    stories = tool.stories.all().order_by('-created')
    context = {'tool': tool, 'tool_followers': tool_followers,
            'stories': stories}

    return render(request, 'tools/show.html', context)


@transaction.atomic
@login_required
def follow(request, tool_id):
    if request.user.has_perm('tools.change_tool'):
        tool = get_object_or_404(Tool, id=tool_id)
    else:
        tool = get_object_or_404(Tool, id=tool_id, published=True)
    if request.method == 'POST':
        should_notify = False
        if request.POST.get('should_notify', '0') == '1':
            should_notify = True
        tfoll, created = ToolFollower.objects.get_or_create(
            user=request.user,
            tool=tool
        )
        tfoll.should_notify = should_notify
        tfoll.save()
        messages.success(request, "You are now following this tool.")
    return redirect(tool)


@login_required
def unfollow(request, tool_id):
    if request.user.has_perm('tools.change_tool'):
        tool = get_object_or_404(Tool, id=tool_id)
    else:
        tool = get_object_or_404(Tool, id=tool_id, published=True)
    if request.method == 'POST':
        tool.followers.all().filter(user_id=request.user.id).delete()
        messages.success(request, "You are no longer following this tool.")
    return redirect(tool)


@transaction.atomic
@permission_required('tools.change_tool', login_url='tools:index')
@login_required
def edit(request, tool_id):
    # TODO: use celery tasks for storage IO so it doesn't block transaction
    tool = get_object_or_404(Tool, id=tool_id)

    categories_ids = list(tool.categories.all().values_list('id', flat=True))
    attributes = {
        'title': tool.title,
        'description': tool.description,
        'resources_text': tool.resources_text,
        'categories': categories_ids,
        'published': tool.published,
    }

    if tool.cover_image and default_storage.exists(tool.cover_image.name):
        files = {'cover_image': tool.cover_image}
    else:
        files = {}
    form = ToolForm(attributes, files)

    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('cover_image-clear'):
                cover_image = None
                if tool.has_existing_cover_image():
                    default_storage.delete(tool.cover_image.name)
            else:
                if form.cleaned_data['cover_image']:
                    if tool.has_existing_cover_image():
                            default_storage.delete(tool.cover_image.name)
                    cover_image = form.cleaned_data['cover_image']
                else:
                    cover_image = tool.cover_image
            tool.published = form.cleaned_data['published']
            tool.title = form.cleaned_data['title']
            tool.description = form.cleaned_data['description']
            tool.resources_text = form.cleaned_data['resources_text']
            tool.cover_image = cover_image
            tool.categories.clear()
            tool.categories.add(*form.cleaned_data['categories'])
            tool.save()

            messages.success(request, "You updated a tool")
            return redirect(tool)

    context = {'tool': tool, 'form': form}
    return render(request, 'tools/edit.html', context)
