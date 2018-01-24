import logging

from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from django.views.generic import View

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from tools.models import Tool, ToolCategory, Story, StoryOverviewPage, ToolOverviewPage, CategoryGroupOverviewPage
from profiles.models import Profile
from .forms import SearchForm, ModelSearchForm


log = logging.getLogger(__name__)

DEFAULT_LIMIT = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE


def get_search_results(modelcls, q, limit=DEFAULT_LIMIT):
    sqs = SearchQuerySet().models(modelcls)
    sqs = sqs.auto_query(q).filter().load_all()
    total_results_count = sqs.count()
    sresults = sqs[:limit]
    results = [ccc.object for ccc in sqs._result_cache[:limit] if ccc]
    return total_results_count, results


def homepage(request): 
    recent_stories = Story.objects.filter(published=True).order_by('-created')[:3]
    recent_tools = Tool.objects.all()[:3]
    overviews = {
        'Work Areas': CategoryGroupOverviewPage.objects.get(pk=1),
        'Stories': StoryOverviewPage.objects.get(pk=1), 
        'Tools': ToolOverviewPage.objects.get(pk=1)
    }
    context = {
        'recent_stories': recent_stories, 
        'recent_tools': recent_tools, 
        'overviews': overviews, 
    }
    return render(request, 'search/index.html', context)

def search_page(request):
    limit = settings.HOMEPAGE_DISPLAY_RESULTS
    q = request.GET.get('q', '')
    if q:
        form = SearchForm({'q': q})
        if form.is_valid():
            q = form.cleaned_data['q']

            tools_results_count, tools =\
                get_search_results(Tool, q, limit=limit)

            categories_results_count, categories =\
                get_search_results(ToolCategory, q, limit=limit)

            stories_results_count, stories =\
                get_search_results(Story, q, limit=limit)
            profiles_results_count, profiles =\
                get_search_results(Profile, q, limit=limit)
        else:
            messages.error(request, "invalid search expression")
    else:
        form = SearchForm()
        tools = Tool.objects.annotate(num_followers=Count('followers'))\
            .filter(published=True).order_by('-num_followers')[:limit]
                
        tools_results_count = len(tools)

        categories = ToolCategory.objects.filter(published=True)\
            .order_by('?')[:limit]
        categories_results_count = len(categories)

        stories = Story.objects.all().order_by('-created')[:limit]
        stories_results_count = len(stories)

        profiles = Profile.objects.filter(user__is_superuser=False)\
            .order_by('-user__date_joined')[:limit]
        profiles_results_count = len(profiles)

    ctx = {
        'query': q,
        'form': form,
        'tools': tools,
        'tools_results_count': tools_results_count,
        'categories': categories,
        'categories_results_count': categories_results_count,
        'stories': stories,
        'stories_results_count': stories_results_count,
        'profiles': profiles,
        'profiles_results_count': profiles_results_count,
    }
    return render(request, 'search/search_index.html', ctx)


class BaseSearchView(View):
    http_method_names = ['get', ]
    form_class = ModelSearchForm
    limit = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        params = {'model': self.model, 'q': request.GET.get('q')}
        form = self.form_class(params)
        if form.is_valid():
            q = form.cleaned_data['q']
            total_results_count, results = self.get_results(q)
        else:
            log.debug(form.errors.as_data())
            messages.error(request, 'invalid search query')
            q = ''
            results = []
            total_results_count = 0
        ctx = {
            'query': q,
            'results': results,
            'total_results_count': total_results_count,
        }
        return render(request, self.template_name, ctx)

    def get_results(self, q):
        raise NotImplementedError


class ToolSearchView(BaseSearchView):
    template_name = "search/tool_results.html"
    model = 'tools.tool'
    model_class = Tool

    def get_results(self, q):
        return get_search_results(self.model_class, q, limit=self.limit)


class StorySearchView(BaseSearchView):
    template_name = "search/story_results.html"
    model = 'tools.story'
    model_class = Story

    def get_results(self, q):
        return get_search_results(self.model_class, q, limit=self.limit)


class ProfileSearchView(BaseSearchView):
    template_name = "search/profile_results.html"
    model = 'profiles.profile'
    model_class = Profile

    def get_results(self, q):
        return get_search_results(self.model_class, q, limit=self.limit)

