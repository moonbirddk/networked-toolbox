import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from .forms import ToolForm
from .models import Tool

log = logging.getLogger(__name__)


def home(request):
    return render(request, 'tools/home.html', {})


def add(request):

    form = ToolForm()

    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
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
    tool = get_object_or_404(Tool, id=tool_id)

    attributes = {'title': tool.title, 'description': tool.description}

    form = ToolForm(attributes)

    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            tool.title = form.cleaned_data['title']
            tool.description = form.cleaned_data['description']
            tool.cover_image = form.cleaned_data['cover_image']
            tool.save()
            messages.success(request, "You updated a tool")
            return redirect('tools:index')

    context = {'tool': tool, 'form': form}
    return render(request, 'tools/edit.html', context)

