from django import forms

from .models import *

from django.contrib.auth import (
    authenticate,
    get_user_model

)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_queryset = User.objects.filter(email=email)

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if email_queryset.exists():
            raise forms.ValidationError(
                'This email has already been registered')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords must match')

        return super(UserRegisterForm, self).clean(*args, **kwargs)


class AddMultipleScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['task', 'acquired_blood_cells']

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


