from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Page
from .forms import PageForm

@login_required
@permission_required('pages.add_page')
def add_page(request):
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = Page.objects.create(**form.cleaned_data)
            page.save()
            messages.success(request, "You created a page")
            return redirect(page)

    context = {
        'form': form
    }
    return render(request, 'pages/add_page.html', context)

@login_required
@permission_required('pages.change_page')
def edit_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    form = PageForm(page.__dict__)

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page.title = form.cleaned_data['title']
            page.slug = form.cleaned_data['slug']
            page.published = form.cleaned_data['published']
            page.content = form.cleaned_data['content']
            page.save()
            messages.success(request, "You edited the '%s' page" % page.title)
            return redirect(page)

    published_pages = Page.objects.filter(published=True)
    drafted_pages = Page.objects.filter(published=False)

    context = {
        'form': form,
        'page': page,
        'published_pages': published_pages,
        'drafted_pages': drafted_pages
    }
    return render(request, 'pages/edit_page.html', context)


def show_page(request, page_slug):
    if request.user.has_perm('pages.change_page'):
        page = get_object_or_404(Page, slug=page_slug)
    else:
        page = get_object_or_404(Page, slug=page_slug, published=True)

    context = {
        'page': page
    }
    return render(request, 'pages/show_page.html', context)
