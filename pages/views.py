from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Page
from .forms import PageForm


def show_page(request, page_slug):
    if request.user.has_perm('pages.change_page'):
        page = get_object_or_404(Page, slug=page_slug)
    else:
        page = get_object_or_404(Page, slug=page_slug, published=True)

    context = {
        'page': page
    }
    return render(request, 'pages/show_page.html', context)
