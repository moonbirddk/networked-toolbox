import logging
from django import forms
from django.db import models

from haystack import forms as haystack_forms
from haystack import models as haystack_models


log = logging.getLogger(__name__)


class SearchForm(forms.Form):
    q = forms.fields.CharField(max_length=30, label='')

    def clean_q(self):
        q = self.cleaned_data.get('q')
        if q:
            newval = q.replace('<', '')\
                .replace('>', '')\
                .replace('%', '')\
                .replace('\'', '')
            self.cleaned_data['q'] = newval
            return newval


class ModelSearchForm(SearchForm):
    model = forms.CharField(
        required=True,
        max_length=20,
        label='model'
    )

    def clean_model(self):
        if self.cleaned_data.get('model'):
            model = self.cleaned_data.get('model')
            hchoices = haystack_forms.model_choices()
            if model in [hch[0] for hch in hchoices]:
                self.cleaned_data['model'] =\
                    models.get_model(*model.split('.'))
                return self.cleaned_data['model']
            raise forms.ValidationError("invalid search model")
