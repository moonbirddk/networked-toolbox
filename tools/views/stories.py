from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from tools.forms import StoryForm
from tools.models import Tool, Story, CategoryGroup
from django.utils.html import format_html
from django.urls import reverse

@login_required
def add_story(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id, published=True)
    form = StoryForm()

    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = Story.objects.create(tool_id=tool.id, user_id=request.user.id, **form.cleaned_data)
            messages.success(request, "You created a story")
            return redirect('tools:show', story.tool_id)
    context = {'tool': tool, 'form': form}
    return render(request, 'stories/add_story.html', context)


@login_required
def add_workarea_story(request, category_group_id):
    category_group = get_object_or_404(CategoryGroup, id=category_group_id, published=True)
    form = StoryForm()

    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.cleaned_data['user']=request.user
            form.cleaned_data['category_group']=category_group
            instance = form.save(commit=False)
            instance.user = request.user
            instance.category_group = category_group
            instance.save()
            form.save_m2m()

            messages.success(request, "You created a story")
            return redirect('tools:show_categorygroup', category_group.id)

    context = {'category_group': category_group, 'form': form}
    return render(request, 'stories/add_workarea_story.html', context)

@login_required
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)
    attributes = {
        'title': story.title,
        'content': story.content,
        'country': story.country,
        'associated_tools': story.associated_tools.all()
    }

    files = {}
    if story.cover_image and \
            default_storage.exists(story.cover_image.name):
        files = {'cover_image': story.cover_image}
   
    form = StoryForm(attributes, files)

    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():

            story.associated_tools=form.cleaned_data['associated_tools']
            story.title = form.cleaned_data['title']
            story.content = form.cleaned_data['content']
            story.country = form.cleaned_data['country']

            story.save()
            messages.success(request, "You edited this story")
            return redirect('tools:show_story', story.id)

    context = {
        'story': story,
        'form': form,

    }
    return render(request, 'stories/edit_story.html', context)


def show_story(request, story_id):
    print (request.GET.get('from'))
    story = get_object_or_404(Story, id=story_id)
    related_model_instance = get_object_or_404(Tool, id=story.tool_id) if story.tool else get_object_or_404(CategoryGroup, id=story.category_group_id)
    related_model_name = related_model_instance._meta.verbose_name
    related_stories = Story.objects.filter(tool_id=story.tool_id).exclude(id=story.id).order_by('-created')[:3]
    associated_tools = story.associated_tools.all()
    stories_home = {
        'ov': format_html('<a href="{}">Stories Of Change</a>',reverse('tools:show_all_stories')), 
        'wa_ov': format_html('<a href="{}">Thematic Areas</a>',reverse('tools:index'))
    }
    parent_of_story = format_html('<a href="{}">{}</a>', related_model_instance.get_absolute_url(),related_model_instance.title)
    breadcrumb_root = stories_home.get(request.GET.get('from'), parent_of_story)
    breadcrumbs = [breadcrumb_root, story.title]
    context = {
        'story': story,
        'related_model_instance': related_model_instance,
        'related_model_name': related_model_name,
        'related_stories': related_stories,
        'resources': associated_tools,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'stories/show_story.html', context)

def show_all_stories(request):
    ##EXTENDABLE
    ORDERINGS = {
        'a_z': ('alphabetically', 'title'),
        'country': ('by country', 'country'),
        'date': ('newest', '-created'),
        'newest_comments': ('recently discussed', 'comments__added_dt'),
    }
    order_name, order_query = ORDERINGS[request.GET.get('order', 'date')]
    stories = Story.objects.filter(published=True).prefetch_related('tool', 'category_group', 'comment_root__comments').order_by(order_query)
    context = {
        'stories': stories,
        'order': order_name,
        'order_by_list': ORDERINGS
    }
    return render(request, 'stories/show_all_stories.html', context)