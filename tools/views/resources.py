import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import default_storage

from tools.forms import ToolForm, ToolResourceForm
from tools.models import Tool, ToolResource

log = logging.getLogger(__name__)

def add_resource(request, tool_id):
    tool = get_object_or_404(Tool,id=tool_id)
    form = ToolResourceForm()

    if request.method == 'POST':
        form = ToolResourceForm(request.POST, request.FILES)
        if form.is_valid():
            ToolResource.objects.create(tool=tool,**form.cleaned_data)
            messages.success(request, "You added a resource")
            return redirect('tools:show', tool.id)

    context = {'form': form, 'tool': tool}
    return render(request, 'tools/add_resource.html', context)


def delete_resource(request, tool_id, resource_id):
    resource = get_object_or_404(ToolResource.objects.select_related('tool'),id=resource_id)
    tool = resource.tool

    if request.method == 'GET':
        context = {'tool': tool, 'resource':resource}
        return render(request, 'tools/delete_resource.html',context)
    else:
        if 'yes' == request.POST.get('confirmation', 'no'):
            resource.delete()
            messages.success(request, "You deleted a resource")
        return redirect('tools:show', tool.id)
