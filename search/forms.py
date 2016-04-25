from django import forms


class SearchForm(forms.Form):
    q = forms.fields.CharField(max_length=30, label='')
