import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType

from .forms import ToolResourceForm, ToolResourceEditForm
from .models import ToolResource

log = logging.getLogger(__name__)

def get_url_for_type_name(type_name, obj_id):
    if type_name == 'tool':
        url = 'tools:show'
    elif type_name == 'toolcategory':
        url = 'tools:show_category'
    return reverse(url, args=(obj_id,))


@permission_required('tools.add_toolresource', login_url='tools:index')
@login_required
def add(request, type_name, type_id):
    content_type = ContentType.objects.get(app_label="tools", model=type_name)
    related_object = get_object_or_404(content_type.model_class(), id=type_id)

    form = ToolResourceForm()

    if request.method == 'POST':
        form = ToolResourceForm(request.POST, request.FILES)
        if form.is_valid():
            ToolResource.objects.create(content_object=related_object,
                **form.cleaned_data)
            messages.success(request, "You added a resource")
            url = get_url_for_type_name(type_name, related_object.id)
            return redirect(url)

    context = {'form': form, 'related_object': related_object, 'type_name':type_name}

    return render(request, 'resources/add.html', context)


@transaction.atomic
@permission_required('tools.delete_toolresource', login_url='tools:index')
@login_required
def delete(request, resource_id):
    resource = get_object_or_404(ToolResource, id=resource_id)
    content_object = resource.content_object

    if request.method == 'GET':
        context = {'content_object': content_object, 'resource': resource}
        return render(request, 'resources/delete.html', context)
    else:
        if 'yes' == request.POST.get('confirmation', 'no'):
            resource.delete()
            messages.success(request, "You deleted a resource")
        return redirect(content_object)

@permission_required('tools.delete_toolresource', login_url='tools:index')
@login_required
def edit(request,resource_id):
    resource = get_object_or_404(ToolResource, id=resource_id)

    if request.method == 'POST':
        form = ToolResourceEditForm(request.POST)
        if form.is_valid():
            resource.title = form.cleaned_data['title']
            resource.save()
            messages.success(request, "You updated a resource")
            return redirect(resource.content_object)
            
    form = ToolResourceEditForm({'title':resource.title})
    context = {'resource': resource, 'form':form}

    return render(request, 'resources/edit.html', context)
