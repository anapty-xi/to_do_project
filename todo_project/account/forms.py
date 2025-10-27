from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label='логин')
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
    username = forms.CharField(label='логин')
    password = forms.CharField(label='пароль', widget=forms.PasswordInput)



class ProfileInfoForm(forms.Form):
    username = forms.CharField(label='логин')
    email = forms.EmailField(label='почта')
    birthd = forms.DateField(label='дата рождения')
    sex = forms.ChoiceField(choices=[('male','м'), ('female','ж')])
    photo = forms.ImageField(required=False)
    preview = forms.CharField(widget=forms.Textarea)




class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='повторите пароль', widget=forms.PasswordInput)

class FortgotPasswordForm(forms.Form):
    email = forms.EmailField(label='почта привязанная к аккаунту')

    def clean_email(self):
        user_email = self.cleaned_data['email']
        try:
            User.objects.get(email=user_email)
            return user_email
        except User.DoesNotExist:
            raise ValidationError('аккаунта с данной почтой не существует')




  

