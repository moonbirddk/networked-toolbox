import logging

from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.db.models import Count

from haystack.query import SearchQuerySet

from tools.models import Tool, ToolCategory, Story
from profiles.models import Profile
from .forms import SearchForm


log = logging.getLogger(__name__)


def get_search_results(modelcls, q, limit=settings.SEARCH_NUM_RESULTS):
    sqs = SearchQuerySet().models(modelcls)
    sqs = sqs.auto_query(q).filter().load_all()
    sresults = sqs[:limit]
    return [ccc.object for ccc in sqs._result_cache]


def homepage(request):
    limit = settings.SEARCH_NUM_RESULTS
    if request.GET and request.GET.get('q'):
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            tools = get_search_results(Tool, q, limit=limit)
            categories = get_search_results(ToolCategory, q, limit=limit)
            stories = get_search_results(Story, q, limit=limit)
            profiles = get_search_results(Profile, q, limit=limit)
        else:
            messages.error(request, "invalid search expression")
    else:
        form = SearchForm()
        tools = Tool.objects.annotate(num_followers=Count('followers'))\
            .order_by('-num_followers')[:limit]
        categories = ToolCategory.objects.all().order_by('?')[:limit]
        stories = Story.objects.all().order_by('-created')[:limit]
        profiles = Profile.objects.all().order_by('-user__date_joined')[:limit]

    ctx = {
        'form': form,
        'tools': tools,
        'categories': categories,
        'stories': stories,
        'profiles': profiles
    }
    return render(request, 'search/index.html', ctx)
