import logging

from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from django.views.generic import View

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from tools.models import Tool, ToolCategory, Story
from profiles.models import Profile
from .forms import SearchForm, ModelSearchForm


log = logging.getLogger(__name__)


def get_search_results(modelcls, q, limit=settings.SEARCH_NUM_RESULTS):
    sqs = SearchQuerySet().models(modelcls)
    sqs = sqs.auto_query(q).filter().load_all()
    sresults = sqs[:limit]
    return [ccc.object for ccc in sqs._result_cache if ccc]


def homepage(request):
    limit = settings.SEARCH_NUM_RESULTS
    q = request.GET.get('q', '')
    if q:
        form = SearchForm({'q': q})
        if form.is_valid():
            q = form.cleaned_data['q']
            log.debug("q: %s", q)
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
        profiles = Profile.objects.filter(user__is_superuser=False)\
            .order_by('-user__date_joined')[:limit]

    ctx = {
        'query': q,
        'form': form,
        'tools': tools,
        'categories': categories,
        'stories': stories,
        'profiles': profiles
    }
    return render(request, 'search/index.html', ctx)


class BaseSearchView(View):
    http_method_names = ['get', ]
    form_class = ModelSearchForm
    limit = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        params = {'model': self.model, 'q': request.GET.get('q')}
        form = self.form_class(params)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = self.get_results(q)
        else:
            log.debug(form.errors.as_data())
            messages.error(request, 'invalid search query')
            q = ''
            results = []
        ctx = {
            'query': q,
            'results': results,
            'results_count': len(results),
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

