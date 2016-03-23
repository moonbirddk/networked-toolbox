import json

from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm
from .utils import build_comment_data


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
            tzstr = request.session.get('django_timezone', settings.TIME_ZONE)
            comment_dict = build_comment_data(comment, tzstr=tzstr)
            ok = True
        else:
            errors = json.loads(form.errors.as_json(escape_html=True))
    data = {
        'ok': ok,
        'errors': errors,
        'comment': comment_dict,
    }
    return JsonResponse(data)
