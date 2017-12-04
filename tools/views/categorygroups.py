
from django.db import transaction
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..models import CategoryGroup, ToolCategory, get_default_category_group_id, CategoryOverviewPage
from ..forms import CategoryGroupForm



def show_categorygroup(request, category_group_id):

    category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    categories = category_group.categories.all().order_by('title')
    context = {
        'category_group': category_group,
        'categories': categories, 

    }
    return render (request, 'tools/show_categorygroup.html', context)
    
    

@permission_required('tools.add_categorygroup', login_url='tools:index')
@login_required
def add_categorygroup(request):
    form = CategoryGroupForm()
    if request.method == 'POST':
        form = CategoryGroupForm(request.POST)
        if form.is_valid():
            cat_group = CategoryGroup.objects\
                .create(name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'])
            ids = [cat.id for cat in form.cleaned_data['categories']]
            ToolCategory.objects.filter(id__in=ids).update(group=cat_group)
            messages.success(request, "You have added the toolbox")
            return redirect(reverse('tools:index'))
    ctx = {
        'form': form,
    }
    return render(request, 'tools/add_categorygroup.html', ctx)


@transaction.atomic
@permission_required('tools.change_categorygroup', login_url='tools:index')
@login_required
def edit_categorygroup(request, category_group_id):
    if category_group_id == '1':
        messages.error(request, "You cannot edit the default toolbox")
        return redirect(reverse('tools:index'))
    categorygroup = get_object_or_404(CategoryGroup, id=category_group_id)
    categories_ids = ToolCategory.objects\
        .filter(group=categorygroup)\
        .values_list('id', flat=True)
    form = CategoryGroupForm(dict(name=categorygroup.name,
                             description=categorygroup.description,
                             categories=categories_ids))
    if request.method == 'POST':
        form = CategoryGroupForm(request.POST)
        if form.is_valid():
            categorygroup.name = form.cleaned_data['name']
            categorygroup.description = form.cleaned_data['description']
            categorygroup.save()
            old_ids_set = set(ToolCategory.objects
                              .filter(group_id=categorygroup.id)
                              .values_list('id', flat=True))
            new_ids_set = set([cat.id for cat in
                               form.cleaned_data['categories']])

            # everything that was removed gets default group id
            default_id = get_default_category_group_id()
            to_default_ids = old_ids_set.difference(new_ids_set)
            ToolCategory.objects.filter(id__in=to_default_ids)\
                .update(group_id=default_id)

            #to_update = old_ids_set.difference(new_ids_set)
            ToolCategory.objects.filter(id__in=new_ids_set)\
                .update(group_id=categorygroup.id)


            messages.success(request, "You have updated the toolbox")
            return redirect(reverse('tools:index'))
    ctx = {
        'form': form,
        'categorygroup': categorygroup,
    }
    return render(request, 'tools/edit_categorygroup.html', ctx)


@transaction.atomic
@permission_required('tools.delete_categorygroup', login_url='tools:index')
@login_required
def delete_categorygroup(request, category_group_id):
    categorygroup = get_object_or_404(CategoryGroup, id=category_group_id)
    if category_group_id == '1':
        messages.error(request, "You can not delete the default toolbox")
        return redirect(reverse('tools:index'))
    ctx = {
        'categorygroup': categorygroup,
    }

    if request.method == 'POST':
        if 'yes' == request.POST.get('confirmation', 'no'):
            categorygroup.delete()
            messages.info(request, "You have deleted the toolbox")
        return redirect(reverse('tools:index'))
    return render(request, 'tools/delete_categorygroup.html', ctx)
