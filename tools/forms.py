from django import forms

class ToolForm(forms.Form):
    title = forms.fields.CharField(max_length=30, required=True)
    description = forms.fields.CharField(max_length=5000, widget=forms.Textarea, required=True)