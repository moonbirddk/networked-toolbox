import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import default_storage

from tools.forms import ToolCategoryForm
from tools.models import Tool, ToolCategory


log = logging.getLogger(__name__)


def list_categories(request):
    categories = ToolCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'tools/list_categories.html', context)


def show_category(request, cat_id):
    category = get_object_or_404(ToolCategory, id=cat_id)
    context = {'category': category}
    return render(request, 'tools/show_category.html', context)


def add_category(request):

    form = ToolCategoryForm()

    if request.method == 'POST':
        form = ToolCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = ToolCategory.objects.create(**form.cleaned_data)
            messages.success(request, "You created a category")
            return redirect('tools:show_category', cat.id)

    context = {'form': form}
    return render(request, 'tools/add_category.html', context)


@transaction.atomic
def edit_category(request, cat_id):
    # TODO: use celery tasks for storage IO so id doesn't block transaction
    category = get_object_or_404(ToolCategory, id=cat_id)

    attributes = {
        'title': category.title,
        'description': category.description,
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
                    if category.cover_image:
                        if category.has_existing_cover_image():
                            default_storage.delete(category.cover_image.name)
                    cover_image = form.cleaned_data['cover_image']
                else:
                    cover_image = category.cover_image

            category.title = form.cleaned_data['title']
            category.description = form.cleaned_data['description']
            category.cover_image = cover_image
            category.save()
            messages.success(request, "You updated a category")
            return redirect('tools:list_categories')

    context = {'category': category, 'form': form}
    return render(request, 'tools/edit_category.html', context)


@transaction.atomic
def delete_category(request, cat_id):
    category = get_object_or_404(ToolCategory, id=cat_id)

    if request.method == 'GET':
        context = {'category': category}
        return render(request, 'tools/delete_category.html', context)
    else:
        if 'yes' == request.POST.get('confirmation', 'no'):
            category.delete()
            messages.success(request, "You deleted a category")
        return redirect('tools:list_categories')
