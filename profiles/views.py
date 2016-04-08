
import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db import transaction

from .forms import ProfileForm
from .models import User, Profile, ActivityEntry
from tools.models import Story, ToolFollower
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http.response import HttpResponseNotFound

from bleach import clean

log = logging.getLogger(__name__)


def terms_and_conditions(request):
    if not settings.DJANGO_ENV == 'staging':
        return HttpResponseNotFound("not found")

    next_page = '/'
    if (REDIRECT_FIELD_NAME in request.POST or
            REDIRECT_FIELD_NAME in request.GET):
        next_page = request.POST.get(REDIRECT_FIELD_NAME,
                                     request.GET.get(REDIRECT_FIELD_NAME))
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = '/'

    if request.method == 'POST':
        if request.POST.get('accepted'):
            resp = HttpResponseRedirect(next_page)
            resp.set_cookie('has_accepted_terms', '1')
            return resp
        else:
            messages.error(request, "Please accept Terms and Conditions")

    ctx = {
        'redirect_field_name': REDIRECT_FIELD_NAME,
        'next_page': next_page,
    }
    resp = render(request, 'profiles/terms_and_conditions.html', ctx)
    resp.set_cookie('has_accepted_terms', '0')
    return resp

def show(request, user_id):
    user = User.objects.get(id=user_id)
    tool_followers = ToolFollower.objects.filter(user_id=user.id).filter(tool__published=True).order_by('?')
    tools = [tf.tool for tf in tool_followers]
    stories = Story.objects.filter(user=user).order_by('-created')
    stories_fav = []
    activities = ActivityEntry.objects.filter(user=user).order_by('-created')
    ctx = {
        'profile_user': user,
        'tools': tools,
        'stories': stories,
        'stories_fav': stories_fav,
        'activities': activities,
    }
    return render(request, 'profiles/show.html', ctx)

def show_tools(request, user_id):
    user = User.objects.get(id=user_id)
    tool_followers = ToolFollower.objects.filter(user_id=user.id).filter(tool__published=True)
    tools = [tf.tool for tf in tool_followers]
    ctx = {
        'profile_user': user,
        'tools': tools,
    }
    return render(request, 'profiles/show_tools.html', ctx)

@login_required
@transaction.atomic
def edit(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    attributes = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': profile.bio,
        'country': profile.country,
    }

    if profile.photo and default_storage.exists(profile.photo.name):
        files = {'photo': profile.photo}
    else:
        files = {}

    form = ProfileForm(attributes, files)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('photo-clear'):
                photo = None
                if profile.has_existing_photo():
                    default_storage.delete(profile.photo.name)
            else:
                if form.cleaned_data['photo']:
                    if profile.has_existing_photo():
                            default_storage.delete(profile.photo.name)
                    photo = form.cleaned_data['photo']
                else:
                    photo = profile.photo
            profile.photo = photo
            profile.bio = clean(form.cleaned_data.get('bio', None), tags=[],
                    strip=True, strip_comments=True)
            profile.country = form.cleaned_data['country']
            profile.save()
            user.first_name = form.cleaned_data.get('first_name', None)
            user.last_name = form.cleaned_data.get('last_name', None)
            user.save()
            messages.success(request, "You have updated your profile.")
            return redirect('profiles:show', user.id)
    ctx = {
        'form': form,
    }
    return render(request, 'profiles/edit.html', ctx)

