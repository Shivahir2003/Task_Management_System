from django.urls import path

from accounts.views import UserLoginView,UserSignupView,userlogoutview,ResetPasswordView

app_name='accounts'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('signup/',UserSignupView.as_view(),name='signup'),
    path('logout/',userlogoutview,name='logout'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset-password')
]