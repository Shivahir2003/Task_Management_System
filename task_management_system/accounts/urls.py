from django.urls import path

from accounts.views import UserLoginView,UserSignupView,userlogoutview,ResetPasswordView,profileview,EditProfileView

app_name='accounts'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('signup/',UserSignupView.as_view(),name='signup'),
    path('logout/',userlogoutview,name='logout'),
    path('profile/',profileview,name='profile'),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset_password')
]