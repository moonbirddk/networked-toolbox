from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from .models import LibraryDocument, OnlineCourse, VideoResource
from allauth.account.decorators import verified_email_required

from itertools import chain

# Create your views here.


def document_index(request):
    documents = LibraryDocument.objects.filter(published=True)
    courses = OnlineCourse.objects.filter(published=True)
    video_resources = VideoResource.objects.filter(published=True)
   # queryset = list(chain(documents, courses, video_resources))
    context = {
        'documents': documents,
        'courses': courses, 
        'video_resources': video_resources, 

    }
    return render(request, 'library_documents/index.html', context)

def show_library_item(request, document_id): 
    template_path = "library_documents/show_{}.html".format(
        request.path.split("/")[2][:-1]
    )
    MODEL_CLASSES = {
        'courses': OnlineCourse,
        'documents': LibraryDocument,
        'video_resources': VideoResource
    }

    model_class = request.path.split("/")[2]
    document = get_object_or_404(MODEL_CLASSES.get(model_class), id=document_id)
    
    context = {
        "document": document, 
        "user": request.user, 
    }
    
    if hasattr(document, "participiants"): 
        context.update(
            user_participates=request.user in document.participiants.all()
        )
    return render(request, template_path, context)


@login_required
@verified_email_required
def course_signup(request, id):
    course = OnlineCourse.objects.get(id=id)
    course.participiants.add(request.user)
    course.save()
    subject = "You have signed up for an Online Course on Reflection Action."
    message = """Dear {} {},
    We have signed you up for the Online Course {}. 
    Thank you very much for your interest.
    
    Kind regards,
    Reflection Action""".format(
        request.user.first_name,
        request.user.last_name,
        course.title,
    )
    request.user.email_user(
        subject,
        message
    )
    return JsonResponse({
        'success': True
    })


@login_required
@verified_email_required
def course_signoff(request, id):
    course = OnlineCourse.objects.get(id=id)
    course.participiants.remove(request.user)
    course.save()
    subject = "You are no longer signed up for an Online Course on Reflection Action."
    message = """Dear {} {},
    We have signed you off of the Online Course {}.
    
    Kind regards,
    Reflection Action""".format(
        request.user.first_name,
        request.user.last_name,
        course.title,
    )
    request.user.email_user(
        subject,
        message
    )

    return JsonResponse({
        'success': True
    })
