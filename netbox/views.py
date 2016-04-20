from django.conf import settings
from django.shortcuts import render
from django.db.models import Count
from tools.models import Story, Tool, ToolCategory
from profiles.models import Profile

def index(request):
    tools = Tool.objects.annotate(num_followers=Count('followers'))\
            .order_by('-num_followers')[:settings.SEARCH_NUM_RESULTS]
    categories = ToolCategory.objects.all().order_by('?')\
            [:settings.SEARCH_NUM_RESULTS]
    stories = Story.objects.all().order_by('-created')\
            [:settings.SEARCH_NUM_RESULTS]
    profiles = Profile.objects.all().order_by('-user__date_joined')\
            [:settings.SEARCH_NUM_RESULTS]

    ctx = {
        'tools': tools,
        'categories': categories,
        'stories': stories,
        'profiles': profiles
    }
    return render(request, 'index.html', ctx)

