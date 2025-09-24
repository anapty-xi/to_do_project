from django import forms
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(label='Юзернейм')
    email = forms.EmailField(label='почта')
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')




class LoginForm(forms.Form):
    username = forms.CharField(label='Юзернейм')
    password = forms.CharField(label='пароль', widget=forms.PasswordInput)

