from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic.base import View

from accounts.models import UserProfile
from accounts.forms import (
    UserSignUpForm,
    UserProfileForm,
    UserLoginForm,
    ResetPasswordForm,
    EditUserForm,
)


class UserAuthenticationView(View):
    """ user authentication class """
    
    def dispatch(self,request,**kwargs):
        if request.path == reverse('accounts:login'):
            return self.login_view(request)
        elif request.path == reverse('accounts:logout'):
            return self.logout_view(request)
        elif request.path == reverse('accounts:signup'):
            return self.signup_view(request)
        elif request.path == reverse('accounts:profile'):
            return self.user_profile_view(request)
        elif request.path == reverse('accounts:edit_profile') :
            return self.edit_user_view(request)
        elif request.path == reverse('accounts:reset_password'):
            return self.change_password_view(request)

    def login_view(self,request):
        """
            User login post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password
            
            Retunrns:
                In Get:
                    render login.html page with empty login form
                In Post:
                    HttpResponseRedirect dashboard url if successful.
                    re-render page with error in validation error
        """
        if request.method == "GET":
            if request.user.is_authenticated:
                return redirect('taskmanager:dashboard')
            else:
                login_form=UserLoginForm()
        elif request.method =="POST":
            login_form=UserLoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data['username']
                password=login_form.cleaned_data['password']

                # check if user is not exists redirect to signup view
                if not User.objects.filter(username=username).exists():
                    messages.error(request,'you have not signed up ')
                    return redirect('accounts:login')

                user = authenticate(request,username=username,password=password)
                if user is None:
                    messages.error(request,'invalid username or password')
                    return redirect('accounts:login')
                else:
                    login(request, user)
                    messages.success(request,f'welcome! {request.user} to Task Manager')
                    return redirect('taskmanager:dashboard')
        return render(request,'accounts/login.html',{'loginform':login_form})

    def logout_view(self,request):
        """
        User logout view
        
        Arguments:
            request (HttpRequest)
        
        Returns:
            render login.html page after logout successfull
        """
        logout(request)
        return redirect('accounts:login')

    def signup_view(self,request):
        """
            User signup post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password,email address, mobile number
            
            Optional Parameters:
                Uesr image
            
            Returns:
                In Get:
                    render signup.html page with empty signup form 
                In Post:
                    HttpResponseRedirect login url if successful.
                    re-render page with error in validation error
        """
        if request.method == "GET":
            if request.user.is_authenticated:
                return redirect('taskmanager:dashboard')
            else:
                user_form=UserSignUpForm()
                userprofile_form=UserProfileForm()
        elif request.method =="POST":
            user_form=UserSignUpForm(request.POST)
            userprofile_form=UserProfileForm(request.POST, request.FILES)

            if user_form.is_valid() and userprofile_form.is_valid():
                user = user_form.save()
                userprofile=userprofile_form.save(commit=False)
                userprofile.user=user
                userprofile.save()
                return redirect('accounts:login')
        context={
                'userform':user_form,
                'profileform':userprofile_form
                }
        return render(request,'accounts/signup.html',context)

    def user_profile_view(self,request):
        """
            Display user detail 
            
            Arguments:
                request (HttpRequest)
            
            Returns:
                render profile.html after login 
        """
        return render(request,"accounts/profile.html")
    
    def edit_user_view(self,request):
        """
            User signup post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password,email address, mobile number
            
            Optional Parameters:
                Uesr image
            
            Returns:
                In Get:
                    get user data from data base and render edit profile page
                In Post:
                    redirect to user profile page if success full
                    re-render page with error in validation error
        """
        try:
            user=User.objects.get(pk=request.user.pk)
            userprofile=UserProfile.objects.get(user=user)
            if request.method == "GET":
                edituser_form=EditUserForm(instance=user)
                editprofile_form=UserProfileForm(instance=userprofile)
            elif request.method =="POST":
                edituser_form=EditUserForm(request.POST,instance=user)
                editprofile_form=UserProfileForm(request.POST, request.FILES,instance=userprofile)
                
                if edituser_form.is_valid() and editprofile_form.is_valid():
                    edituser_form.save()
                    editprofile_form.save()
                    messages.success(request,'Profile updated successfully')
                    return redirect("accounts:profile")
            context={
                    'userform':edituser_form,
                    'profileform':editprofile_form
                }
            return render(request,'accounts/update_profile.html',context)
        except User.DoesNotExist:
            return render(request,'error_404.html')
        except UserProfile.DoesNotExist:
            return render(request,'error_404.html')

    def change_password_view(self,request):
        """
            Reset password post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                current password, new password, confirm password 
            
            Returns:
                In Get:
                    render change password page
                In Post:
                    redirect to login page if succesfull
                    re-render page with error in validation error

        """
        try:
            user =User.objects.get(username=request.user.username)
            if request.method == "GET":
                 resetpassword_form=ResetPasswordForm()
            elif request.method =="POST":
                resetpassword_form=ResetPasswordForm(request.POST)
                if resetpassword_form.is_valid():
                    current_password=resetpassword_form.cleaned_data['current_password']
                    new_password=resetpassword_form.cleaned_data['new_password']

                    if not user.check_password(current_password):
                        resetpassword_form.add_error('current_password',"current password does not match")
                    elif current_password == new_password:
                        resetpassword_form.add_error('new_password',"new password is same as current password")
                    else:
                        user.set_password(new_password)
                        user.save()
                        messages.success(request,"password is changed")
                        return redirect('accounts:logout')
            return render(request,'accounts/reset_password.html',{'resetpassform':resetpassword_form})
        except User.DoesNotExist:
            return render(request,"error_404.html")