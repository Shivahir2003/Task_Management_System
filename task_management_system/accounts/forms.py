import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PASSWORD_FORMAT= r"^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"

class UserSignUpForm(UserCreationForm):
    """ Create User form 

        extends:
            UserCreationForm
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email','first_name','last_name']


    def clean(self):
        form_data= self.cleaned_data
        username=form_data['username']
        password=form_data['password1']

        if username is None:
            self.add_error('username','user already exists')
        elif not re.match(PASSWORD_FORMAT,password):
            self.add_error('password1','password is not valid')
        return form_data

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
    current_password = forms.CharField(max_length=8,widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=8,widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=8,widget=forms.PasswordInput())

    def clean(self):
        form_data=self.cleaned_data
        new_password=form_data['new_password']
        confirm_password=form_data['confirm_password']

        if not re.match(PASSWORD_FORMAT,new_password):
            self.add_error('new_password','password is not valid')
        elif new_password!=confirm_password:
            self.add_error("confirm_password","does not match with new password")

        return form_data
