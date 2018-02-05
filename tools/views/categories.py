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

from django.urls import reverse
from django.utils.html import format_html

log = logging.getLogger(__name__)

def list_categories(request):
    if request.user.has_perm('tools.change_toolcategory'):
        queryset = ToolCategory.objects.all().order_by('-published', 'group', '-order')
    else:
        queryset = ToolCategory.objects.filter(published=True)\
            .order_by('group', '-order')
    cat_filter = PublishedFilter(request.GET, queryset=queryset)

    categories_by_group = CategoryGroup.objects\
        .prefetch_related(Prefetch('categories', queryset=cat_filter.qs))\
        .order_by('name')

    default_id = get_default_category_group_id()
    default_category = categories_by_group.get(id=default_id)
    categories_by_group = list(categories_by_group.exclude(id=default_id))\
            + [default_category]

    overview = CategoryGroupOverviewPage.get_solo()
    context = {
        'categories_filter': cat_filter,
        'overview': overview,
        'categories_by_group': categories_by_group,
    }
    return render(request, 'workareas/list_workareas.html', context)


def show_category(request, cat_id):
    if request.user.has_perm('tools.change_toolcategory'):
        category = get_object_or_404(ToolCategory, id=cat_id)
    else:
        category = get_object_or_404(ToolCategory, id=cat_id, published=True)
    work_areas_list_link =  format_html('<a href="{}">Work Areas</a>', reverse('tools:index'))  
    work_area_link = format_html('<a href="{}">{}</a>', category.group.get_absolute_url(), category.group.name)
    breadcrumbs = [
        work_areas_list_link, 
        work_area_link, 
        category
    ]
    context = {
        'breadcrumbs': breadcrumbs,
        'category': category
    }
    return render(request, 'toolboxes/show_toolbox.html', context)

