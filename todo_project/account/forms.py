from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from todo_project import settings


class RegisterForm(forms.Form):
    username = forms.CharField(label='Юзернейм')
    email = forms.EmailField(label='почта')
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='повторите пароль', widget=forms.PasswordInput)


    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            User.objects.get(username=data)
            raise ValidationError('имя пользователя занято')
        except User.DoesNotExist:
            return data
        
    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            raise ValidationError('аккаунт с данной почтой существует')
        except User.DoesNotExist:
            return data

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')




class LoginForm(forms.Form):
    username = forms.CharField(label='Юзернейм')
    password = forms.CharField(label='пароль', widget=forms.PasswordInput)



class ProfileInfoForm(forms.Form):

    SEX_CHOISES = {
        'M': 'male',
        'Ж': 'female',
        '-': 'default',     
    }

    sex = forms.ChoiceField(choices=SEX_CHOISES)
    birthd = forms.DateField(required=False)
    photo = forms.ImageField(required=False)
    preview = forms.CharField(max_length=300)

