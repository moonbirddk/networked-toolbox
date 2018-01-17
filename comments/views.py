import logging
import json

from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import ThreadedComment, CommentLike
from .forms import CommentForm
from .utils import build_comment_data


log = logging.getLogger(__name__)


@login_required
def add(request):
    errors = {}
    ok = False
    comment_dict = {}
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            log.debug(form.cleaned_data)
            tree_id = None
            if form.cleaned_data['parent']:
                tree_id = form.cleaned_data['parent'].id
            comment = ThreadedComment.objects.create(
                author=request.user,
                content=form.cleaned_data['content'],
                related_object=form.cleaned_data['related_object'],
                parent=form.cleaned_data['parent'],
                tree_id=tree_id
            )
            if not comment.tree_id:
                comment.tree_id = comment.id
                comment.save()
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


@transaction.atomic
@login_required
def like_comment(request, comment_id):
   
    comment = get_object_or_404(ThreadedComment, id=comment_id)
    comment_like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        ) 
    messages.success(request, "You like this comment.")
    url = comment.related_object.get_absolute_url() + '#comments'
    return redirect(url)


@login_required
def unlike_comment(request, comment_id):
    comment = get_object_or_404(ThreadedComment, id=comment_id)
    comment.likes.all().filter(user_id=request.user.id).delete()
    messages.success(request, "You are no longer liking this comment.")
    url = comment.related_object.get_absolute_url()+ '#comments'
    return redirect(url)