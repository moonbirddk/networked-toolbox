import json

from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm


@transaction.atomic
@login_required
def add(request):
    errors = {}
    ok = False
    comment_dict = {}
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=request.user,
                content=form.cleaned_data['content'],
                related_object=form.cleaned_data['related_object']
            )
            comment_dict = comment.to_data()
            ok = True
        else:
            errors = json.loads(form.errors.as_json(escape_html=True))
    data = {
        'ok': ok,
        'errors': errors,
        'comment': comment_dict,
    }
    return JsonResponse(data)
