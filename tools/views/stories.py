
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from tools.forms import StoryForm
from tools.models import Tool, Story, CategoryGroup

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
    }

    files = {}
    if story.cover_image and \
            default_storage.exists(story.cover_image.name):
        files = {'cover_image': story.cover_image}
    print (files)
    form = StoryForm(attributes, files)

    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            

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
    story = get_object_or_404(Story, id=story_id)
    related_model_instance = get_object_or_404(Tool, id=story.tool_id) if story.tool else get_object_or_404(CategoryGroup, id=story.category_group_id)
    related_model_name = related_model_instance._meta.verbose_name
    related_stories = Story.objects.filter(tool_id=story.tool_id).exclude(id=story.id).order_by('-created')[:3]
    context = {
        'story': story, 
        'related_model_instance': related_model_instance, 
        'related_model_name': related_model_name, 
        'related_stories': related_stories 
    }
    return render(request, 'stories/show_story.html', context)

def show_all_stories(request): 
    ##EXTENDABLE 
    ORDERINGS = {
        'a_z': ('alphabetically', 'title'), 
        'country': ('by country', 'country'),
        'date': ('newest', 'created'),
    }
    order = ORDERINGS[request.GET.get('order')] if request.GET.get('order') in ORDERINGS.keys() else ORDERINGS['date']
    stories = Story.objects.all().order_by(order[1])
    context = {
        'stories': stories, 
        'order': order[0],
        'order_by_list': ORDERINGS
    }
    return render(request, 'stories/show_all_stories.html', context)