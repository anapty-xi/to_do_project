from django import forms


class FriendSearchForm(forms.Form):
    username = forms.CharField(max_length=64, label='поиск по логину')