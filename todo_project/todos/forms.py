from django import forms


class TodoAddForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)