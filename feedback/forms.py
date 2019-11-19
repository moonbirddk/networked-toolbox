from django.forms import ModelForm
from django import forms
from trumbowyg.widgets import TrumbowygWidget

from .models import Feedback


class FeedbackForm(ModelForm):
    
    class Meta: 
        model = Feedback
        fields = ['headline', 'text']
        