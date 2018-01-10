
from django.db import transaction
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..models import CategoryGroup, CategoryGroupFollower, ToolCategory, get_default_category_group_id, CategoryOverviewPage
from ..forms import CategoryGroupForm



def show_categorygroup(request, category_group_id):

    category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    categories = category_group.categories.all().order_by('title')
    category_group_follower_ids = list(category_group.followers.all().values_list('user_id', flat=True))

    context = {
        'category_group': category_group,
        'categories': categories, 
        'stories': category_group.stories.all(), 
        'category_group_follower_ids': category_group_follower_ids,
        
    }
    return render (request, 'category_groups/show_categorygroup.html', context)
    
    

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
    return render(request, 'category_groups/add_categorygroup.html', ctx)


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
    return render(request, 'category_groups/edit_categorygroup.html', ctx)


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
    return render(request, 'category_groups/delete_categorygroup.html', ctx)


@transaction.atomic
@login_required
def follow_category_group(request, category_group_id):
    if request.user.has_perm('category_groups.change_category_group'):
        category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    else:
        category_group = get_object_or_404(CategoryGroup, id=category_group_id, published=True)
    if request.method == 'POST':
        should_notify = False
        if request.POST.get('should_notify', '0') == '1':
            should_notify = True
        category_group_follower, created = CategoryGroupFollower.objects.get_or_create(
            user=request.user,
            category_group=category_group
        )
        category_group_follower.should_notify = should_notify
        category_group_follower.save()
        messages.success(request, "You are now following this Work Area.")
    return redirect(category_group)


@login_required
def unfollow_category_group(request, category_group_id):
    if request.user.has_perm('category_groups.change_category_group'):
        category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    else:
        category_group = get_object_or_404(CategoryGroup, id=category_group_id, published=True)
    if request.method == 'POST':
        category_group.followers.all().filter(user_id=request.user.id).delete()
        messages.success(request, "You are no longer following this Work Area.")
    return redirect(category_group)