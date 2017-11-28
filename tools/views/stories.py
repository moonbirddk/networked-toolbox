
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tools.forms import StoryForm
from tools.models import Tool, Story

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

def show_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    tool = get_object_or_404(Tool, id=story.tool_id)
    related_stories = Story.objects.filter(tool_id=story.tool_id).exclude(id=story.id).order_by('-created')[:3]
    context = {'story': story, 'tool': tool, 'related_stories': related_stories }
    return render(request, 'tools/show_story.html', context)
