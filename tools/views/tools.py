import logging
from copy import deepcopy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import default_storage

from tools.forms import ToolForm
from tools.models import Tool, ToolCategory


log = logging.getLogger(__name__)


def home(request):
    return render(request, 'tools/home.html', {})


@transaction.atomic
def add(request):

    form = ToolForm()

    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            log.debug(form.cleaned_data)
            data = deepcopy(form.cleaned_data)
            categories_ids = data.get('categories', [])
            del data['categories']
            tool = Tool.objects.create(**data)
            for cat_id in categories_ids:
                cat = ToolCategory.objects.get(id=cat_id)
                tool.categories.add(cat)
            tool.save()
            messages.success(request, "You created a tool")
            return redirect('tools:index')

    context = {'form': form}
    return render(request, 'tools/add.html', context)


def index(request):
    tools = Tool.objects.all()
    context = {'tools': tools}
    return render(request, 'tools/index.html', context)


def show(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)

    context = {'tool': tool}
    return render(request, 'tools/show.html', context)


@transaction.atomic
def edit(request, tool_id):
    # TODO: use celery tasks for storage IO so id doesn't block transaction
    tool = get_object_or_404(Tool, id=tool_id)

    attributes = {
        'title': tool.title,
        'description': tool.description,
        'categories': tool.categories.values_list('id', flat=True).all(),
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
                    if tool.cover_image:
                        if tool.has_existing_cover_image():
                            default_storage.delete(tool.cover_image.name)
                    cover_image = form.cleaned_data['cover_image']
                else:
                    cover_image = tool.cover_image

            tool.title = form.cleaned_data['title']
            tool.description = form.cleaned_data['description']
            tool.cover_image = cover_image
            tool.save()
            tool.categories.clear()
            for cat_id in form.cleaned_data['categories']:
                cat = ToolCategory.objects.get(id=cat_id)
                tool.categories.add(cat)

            messages.success(request, "You updated a tool")
            return redirect('tools:index')

    context = {'tool': tool, 'form': form}
    return render(request, 'tools/edit.html', context)
