import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import default_storage

from .forms import ToolForm, ToolModelForm
from .models import Tool


log = logging.getLogger(__name__)


def home(request):
    return render(request, 'tools/home.html', {})


def add(request):

    form = ToolModelForm()

    if request.method == 'POST':
        form = ToolModelForm(request.POST, request.FILES)
        if form.is_valid():
            tool = Tool.objects.create(**form.cleaned_data)
            messages.success(request, "You created a tool")
            return redirect('tools:index')

    context = {'form': form}
    return render(request, 'tools/add.html', context)


def index(request):
    tools = Tool.objects.all()
    context = {'tools': tools}
    return render(request, 'tools/index.html', context)


@transaction.atomic
def edit(request, tool_id):
    # TODO: use celery tasks for storage IO so id doesn't block transaction
    tool = get_object_or_404(Tool, id=tool_id)

    attributes = {
        'title': tool.title,
        'description': tool.description,
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
                if default_storage.exists(tool.cover_image.name):
                    default_storage.delete(tool.cover_image.name)
            else:
                if form.cleaned_data['cover_image']:
                    if tool.cover_image:
                        if default_storage.exists(tool.cover_image.name):
                            default_storage.delete(tool.cover_image.name)
                    cover_image = form.cleaned_data['cover_image']
                else:
                    cover_image = tool.cover_image

            tool.title = form.cleaned_data['title']
            tool.description = form.cleaned_data['description']
            tool.cover_image = cover_image
            tool.save()
            messages.success(request, "You updated a tool")
            return redirect('tools:index')

    context = {'tool': tool, 'form': form}
    return render(request, 'tools/edit.html', context)
