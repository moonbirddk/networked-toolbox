from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..forms import OverviewPageForm

from django.contrib.auth.decorators import login_required, permission_required
from ..models import ToolOverviewPage, CategoryOverviewPage

@permission_required('tools.add_toolcategory')
@login_required
def edit_overview(request):
    cat_overview  = CategoryOverviewPage.get_solo()
    tool_overview = ToolOverviewPage.get_solo()

    if request.method == 'POST':
        if 'cat' in request.POST:
            current_overview = cat_overview
            route = 'tools:list_categories'
        elif 'tool' in request.POST:
            current_overview = tool_overview
            route = 'tools:index'

        form = OverviewPageForm(request.POST)
        if form.is_valid():
            current_overview.description = form.cleaned_data['description']
            current_overview.save()

        messages.success(request, "You changed an overview page.")
        return redirect(route)


    tool_form = OverviewPageForm({
        'description': tool_overview.description
    })
    cat_form = OverviewPageForm({
        'description': cat_overview.description
    })

    context = {'cat_form': cat_form, 'tool_form': tool_form}
    return render(request, 'tools/edit_overview.html', context)
