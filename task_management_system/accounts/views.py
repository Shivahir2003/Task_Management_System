from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.base import View

from accounts.forms import UserSignUpForm,UserProfileForm,UserLoginForm,ResetPasswordForm
from accounts.models import UserProfile


class UserLoginView(View):
    """ 
        User Login View Class
        
    """
    def get(self,request):
        """
            User login get method
            
            Arguments:
                request (HttpRequest)
            
            Retunrns:
                render login.html page with empty login form
        """
        login_form=UserLoginForm()
        return render(request,'accounts/login.html',{'loginform':login_form})

    def post(self,request):
        """
            User login post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password
            
            Retunrns:
                HttpResponseRedirect: task_manager.html is successful.
                render login.html page with validation error 
        """
        login_form=UserLoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']

            # check if user is not exists redirect to signup view
            if not User.objects.filter(username=username).exists():
                messages.error(request,'you have not signed up ')
                return redirect('accounts:signup')

            user = authenticate(request,username=username,password=password)
            if user is None:
                messages.error(request,'invalid username or password')
                return redirect('accounts:login')
            else:
                login(request, user)
                messages.success(request,"you have loggin successfully")
                return redirect('accounts:login')
        return render(request,'accounts/login.html',{'loginform':login_form})


class UserSignupView(View):
    """
        User Signup View Class
    """
    def get(self,request):
        """
            User signup get method
            
            Arguments:
                request (HttpRequest)

            Returns:
                render signup.html page with empty signup form 
        """
        user_form=UserSignUpForm()
        userprofile_form=UserProfileForm()
        context={
            'userform':user_form,
            'profileform':userprofile_form
            }
        return render(request,'accounts/signup.html',context)

    def post(self, request):
        """
            User signup post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password,email address, mobile number
            
            Optional Parameters:
                Uesr image
            
            Returns:
                render signup.html page with validatoin error
        """
        user_form=UserSignUpForm(request.POST)
        userprofile_form=UserProfileForm(request.POST, request.FILES)
        context={
            'userform':user_form,
            'profileform':userprofile_form
            }

        if user_form.is_valid() and userprofile_form.is_valid():
            username=userprofile_form.cleaned_data['username']
            mobile_number=userprofile_form.cleaned_data['mobile_number']
            user_image=userprofile_form.cleaned_data['user_image']

            # check if user is exists then redirect to login view
            if User.objects.filter(username=username).exists():
                messages.error(request,'you have already signed up ')
                return redirect('accounts:login')

            # creating user 
            user = user_form.save()
            UserProfile.objects.create(
                user=user,
                mobile_number=mobile_number,
                user_image=user_image
            )
            return redirect('accounts:login')
        return render(request,'accounts/signup.html',context)


class ResetPasswordView(LoginRequiredMixin,View):
    """
        Reset Password View Class
    """
    login_url='accounts:login'

    def get(self,request):
        """
            Reset password get method
            
            Arguments:
                request (HttpRequest)

            Returns:
                render reset_password.html page with empty password reset form
        """
        resetpassword_form=ResetPasswordForm()
        return render(request,'accounts/reset_password.html',{'resetpassform':resetpassword_form})

    def post(self,request):
        """
            Reset password post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                current password, new password, confirm password 
            
            Returns:
                render reset_password.html page with validation error
        """
        try:
            user =User.objects.get(username=request.user.username)
            resetpassword_form=ResetPasswordForm(request.POST)
            if resetpassword_form.is_valid():
                current_password=resetpassword_form.cleaned_data['old_password']
                new_password=resetpassword_form.cleaned_data['new_password']

                if not user.check_password(current_password):
                    messages.error(request,"current password does not match")
                elif current_password == new_password:
                    messages.error(request,"new password is same as current password")
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,"password is changed")
                    return redirect('accounts:logout')
            return render(request,'accounts/reset_password.html',{'resetpassform':resetpassword_form})
        except User.DoesNotExist:
            return HttpResponse("user not found")

@login_required(login_url='accounts:login')
def userlogoutview(request):
    """
        User logout view
        
        Arguments:
            request (HttpRequest)
        
        Returns:
            render login.html page after logout successfull
    """
    logout(request)
    return redirect('accounts:login')
