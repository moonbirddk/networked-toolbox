from django.shortcuts import render
from .models import Page

def show(request, page_slug):
    if request.user.has_perm('pages.change_page'):
        page = get_object_or_404(Page, slug=page_slug)
    else:
        topageol = get_object_or_404(Page, slug=page_slug, published=True)
    context = {
        'page': page
    }
    return render(request, 'pages/show.html', context)
