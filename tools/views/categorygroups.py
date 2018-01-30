
from django.db import transaction
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from tools.filters import PublishedFilter
from django.db.models import Prefetch

from ..models import CategoryGroup, CategoryGroupFollower, ToolCategory, get_default_category_group_id, CategoryOverviewPage, CategoryGroupOverviewPage, Story
from ..forms import CategoryGroupForm



def list_category_groups(request):
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
    ORDERINGS = {
        'a_z': ('alphabetically', 'title'), 
        'created': ('recently added', 'created_date'),
        'newest_comments': ('recently discussed', 'comments__added_dt'),
        'most_followed': ('most followed', 'followers'), 
        'most_used': ('most used', 'users')
    }
    order_name, order_query = ORDERINGS[request.GET.get('order', 'a_z')]
    context = {
        'categories_filter': cat_filter,
        'overview': overview,
        'categories_by_group': categories_by_group,
        'stories': Story.objects.all().order_by('-created'),
        'order': order_name,
        'order_by_list': ORDERINGS
    }
    #return render(request, 'category_groups/list_categorygroups.html', context) OLD PATH
    return render(request, 'workareas/list_workareas.html', context)

def show_categorygroup(request, category_group_id):

    category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    categories = category_group.categories.all().order_by('title')
    category_group_follower_ids = list(category_group.followers.all().values_list('user_id', flat=True))
    breadcrumbs = [
        'Work areas',
        category_group.name
    ]
    context = {
        'category_group': category_group,
        'categories': categories, 
        # 'stories': category_group.stories.filter(published=True), 
        'stories': category_group.stories.all(),  #WTODO
        'category_group_follower_ids': category_group_follower_ids,
        'breadcrumbs': breadcrumbs
        
    }
    #return render (request, 'category_groups/show_categorygroup.html', context)
    return render (request, 'workareas/show_workarea.html', context)
    
    

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