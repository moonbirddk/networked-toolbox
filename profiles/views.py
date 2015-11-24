
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db import transaction

from .forms import ProfileForm
from .models import Profile


@login_required
@transaction.atomic
def profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    attributes = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    if profile.photo and default_storage.exists(profile.photo.name):
        files = {'photo': profile.photo}
    else:
        files = {}

    form = ProfileForm(attributes, files)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.photo = form.cleaned_data.get('photo', None)
            profile.save()
            user.first_name = form.cleaned_data.get('first_name', None)
            user.last_name = form.cleaned_data.get('last_name', None)
            user.save()
            messages.success(request, "You have updated your profile.")
            return redirect('profiles:profile')
    ctx = {
        'form': form,
    }
    return render(request, 'profiles/profile.html', ctx)