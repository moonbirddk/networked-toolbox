
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from tools.filters import PublishedFilter
from django.db.models import Prefetch
from django.utils.html import format_html
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
        .prefetch_related(Prefetch('categories', queryset=cat_filter.qs)).order_by('name')

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
        'overview': overview,
        'categories_by_group': categories_by_group,
        'stories': Story.objects.filter(published=True).order_by('-created'),
        'order': order_name,
        'order_by_list': ORDERINGS
    }
    return render(request, 'workareas/list_workareas.html', context)

def show_categorygroup(request, category_group_id):

    category_group = get_object_or_404(CategoryGroup, id=category_group_id)
    categories = category_group.categories.all().order_by('title')
    category_group_follower_ids = list(category_group.followers.all().values_list('user_id', flat=True))
    work_areas_list_link =  format_html('<a href="{}">Work Areas</a>', reverse('tools:index'))  

    breadcrumbs = [
        work_areas_list_link, 
        category_group.title
    ]
    context = {
        'category_group': category_group,
        'categories': categories,
        'meta': category_group._meta,  
        # 'stories': category_group.stories.filter(published=True), 
        'stories': category_group.stories.all(),  #WTODO
        'category_group_follower_ids': category_group_follower_ids,
        'breadcrumbs': breadcrumbs
        
    }
    return render (request, 'workareas/show_workarea.html', context)
    
    


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