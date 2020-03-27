
from .models import FooterTextblock, SearchBarInfoText


def footer_text_processor(request):
    footer_text = FooterTextblock.objects.get()
    search_text = SearchBarInfoText.objects.get()
    return {
        'footer_text': footer_text, 
        'search_text': search_text, 
    }
