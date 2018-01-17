import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from tools.filters import PublishedFilter
from tools.forms import ToolCategoryForm
from tools.models import ToolCategory, CategoryGroupOverviewPage,\
    CategoryGroup, get_default_category_group_id

log = logging.getLogger(__name__)





def show_category(request, cat_id):
    if request.user.has_perm('tools.change_toolcategory'):
        category = get_object_or_404(ToolCategory, id=cat_id)
    else:
        category = get_object_or_404(ToolCategory, id=cat_id, published=True)
    context = {'category': category}
    return render(request, 'categories/show_category.html', context)


@permission_required('tools.add_toolcategory', login_url='tools:index')
@login_required
def add_category(request, group_category_id=None):
    if group_category_id: 

        form = ToolCategoryForm(initial={'group':group_category_id})
    else:
        form = ToolCategoryForm()

    if request.method == 'POST':
        form = ToolCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = ToolCategory.objects.create(**form.cleaned_data)
            messages.success(request, "You created a toolbox")
            return redirect('tools:show_category', cat.id)

    context = {'form': form}
    return render(request, 'categories/add_category.html', context)


@transaction.atomic
@permission_required('tools.change_toolcategory', login_url='tools:index')
@login_required
def edit_category(request, cat_id):
    # TODO: use celery tasks for storage IO so id doesn't block transaction
    category = get_object_or_404(ToolCategory, id=cat_id)

    attributes = {
        'title': category.title,
        'description': category.description,
        'published': category.published,
        'resources_text': category.resources_text,
        'group': category.group.id,
    }

    if category.cover_image and \
            default_storage.exists(category.cover_image.name):
        files = {'cover_image': category.cover_image}
    else:
        files = {}
    form = ToolCategoryForm(attributes, files)

    if request.method == 'POST':
        form = ToolCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('cover_image-clear'):
                cover_image = None
                if category.has_existing_cover_image():
                    default_storage.delete(category.cover_image.name)
            else:
                if form.cleaned_data['cover_image']:
                    if category.has_existing_cover_image():
                            default_storage.delete(category.cover_image.name)
                    cover_image = form.cleaned_data['cover_image']
                else:
                    cover_image = category.cover_image

            category.published = form.cleaned_data['published']
            category.title = form.cleaned_data['title']
            category.description = form.cleaned_data['description']
            category.cover_image = cover_image
            category.resources_text = form.cleaned_data['resources_text']
            category.group = form.cleaned_data['group']
            category.save()
            messages.success(request, "You updated this toolbox")
            return redirect('tools:show_category', category.id)

    context = {'category': category, 'form': form}
    return render(request, 'categories/edit_category.html', context)


@transaction.atomic
@permission_required('tools.delete_toolcategory', login_url='tools:index')
@login_required
def delete_category(request, cat_id):
    category = get_object_or_404(ToolCategory, id=cat_id)

    if request.method == 'GET':
        context = {'category': category}
        return render(request, 'categories/delete_category.html', context)
    else:
        if 'yes' == request.POST.get('confirmation', 'no'):
            category.delete()
            messages.success(request, "You deleted a toolbox")
        return redirect('tools:index')
