
from django.shortcuts import render, redirect
from django.contrib import messages

from ..models import Suggestion
from ..forms import SuggestionForm, SuggestionRelatedObjectForm
from ..tasks import send_suggestion
from django.http.response import Http404
from django.contrib.auth.decorators import login_required


@login_required
def add_suggestion(request, related_object_type, related_object_id):
    related_form = SuggestionRelatedObjectForm(dict(
        related_object_type=related_object_type,
        related_object=related_object_id
    ))
    if not related_form.is_valid():
        raise Http404()
    form = SuggestionForm()
    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            related_object = related_form.cleaned_data['related_object']
            suggestion = Suggestion(
                description=form.cleaned_data['description'],
                attachement=form.cleaned_data['attachement'],
                related_object=related_object,
                author=request.user
            )
            suggestion.save()
            send_suggestion(suggestion_id=suggestion.id)
            msg = "Your suggestion has been send to administrator"
            messages.info(request, msg)
            print(related_object.get_absolute_url())
            return redirect(related_object)

    ctx = {
        'form': form,
        'related_object_type': related_form.cleaned_data['related_object_type'],
        'related_object': related_form.cleaned_data['related_object'],
    }
    return render(request, 'tools/add_suggestion.html', ctx)