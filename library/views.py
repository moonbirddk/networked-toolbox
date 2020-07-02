from django.shortcuts import render, get_object_or_404
from .models import LibraryDocument, OnlineCourse, VideoResource
from django.contrib.contenttypes.models import ContentType
from itertools import chain
# Create your views here.


def document_index(request):
    documents = LibraryDocument.objects.filter(published=True)
    courses = OnlineCourse.objects.filter(published=True)
    viodeo_resources = VideoResource.objects.filter(published=True)
    queryset = list(chain(documents, courses, viodeo_resources))
    context = {
        'documents': queryset,

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
    
    return render(request, template_path, context)

