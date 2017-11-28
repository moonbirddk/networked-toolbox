from django.shortcuts import render, redirect
from django.contrib import messages

from ..forms import OverviewPageForm

from django.contrib.auth.decorators import login_required, permission_required
from ..models import ToolOverviewPage, CategoryOverviewPage
from django.http.response import HttpResponseNotFound


@permission_required('tools.add_toolcategory')
@login_required
def edit_overview(request, obj_type_name):

    if obj_type_name == 'category':
        overview = CategoryOverviewPage.get_solo()
        route = 'tools:list_categories'
    elif obj_type_name == 'tool':
        overview = ToolOverviewPage.get_solo()
        route = 'tools:index'
    else:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = OverviewPageForm(request.POST)
        if form.is_valid():
            overview.description = form.cleaned_data['description']
            overview.save()
            messages.success(request, "You have changed the overview page.")
            return redirect(route)
        messages.success(request, "Please correct errors.")
    else:
        form = OverviewPageForm({
            'description': overview.description
        })

    context = {
        'form': form,
        'obj_type_name': obj_type_name,
    }
    return render(request, 'tools/edit_overview.html', context)
