from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist

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
                raise forms.ValidationError('Incorrect credentials')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'nickname',
            'password',
            'confirm_password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_queryset = User.objects.filter(email=email)

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nickname = self.cleaned_data.get('nickname')

        try:
            student = Student.objects.get(
                first_name=first_name,
                last_name=last_name,
                nickname=nickname
            )
        except ObjectDoesNotExist:
            student = None

        if email_queryset.exists():
            raise forms.ValidationError(
                'This email has already been registered')

        if not student:
            raise forms.ValidationError(
                'You are not in database. Check the spelling and try again.'
                ' If the problem persists ask your lecturer for help.')

        if student.user:
            raise forms.ValidationError(
                'There already is an account for this student'
            )

        if password != confirm_password:
            raise forms.ValidationError('Passwords must match')

        return super(UserRegisterForm, self).clean(*args, **kwargs)


class AddMultipleScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['task', 'acquired_blood_cells']

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]  # include fields
