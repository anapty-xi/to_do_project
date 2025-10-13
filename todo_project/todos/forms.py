from django import forms


class TodoAddAndEditForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)


class ReportAddForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)