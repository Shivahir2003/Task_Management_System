from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile


class UserSignUpForm(UserCreationForm):
    """ Create User form 

        extends:
            UserCreationForm
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email','first_name','last_name']


class UserProfileForm(forms.Form):
    """
        Create user profile form
    """
    mobile_number = forms.CharField(max_length=10,required=True)
    user_image = forms.FileField(required=False)


class UserLoginForm(forms.Form):
    """
        Login user form
    """
    username = forms.CharField(max_length=10,required=True)
    password = forms.CharField(max_length=8,
                               required=True,
                               widget=forms.PasswordInput())


class ResetPasswordForm(forms.Form):
    """
        Change password form
    """
    old_password = forms.CharField(max_length=8,widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=8,widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=8,widget=forms.PasswordInput())
