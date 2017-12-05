
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    return render(request, 'tools/add_story.html', context)

@login_required
def add_workarea_story(request, category_group_id):
    category_group = get_object_or_404(CategoryGroup, id=category_group_id, published=True)
    form = StoryForm()

    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = Story.objects.create(category_group=category_group, user_id=request.user.id, **form.cleaned_data)
            messages.success(request, "You created a story")
            return redirect('tools:show_categorygroup', story.category_group.id)

    context = {'category_group': category_group, 'form': form}
    return render(request, 'tools/add_workarea_story.html', context)

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
    return render(request, 'tools/show_story.html', context)
