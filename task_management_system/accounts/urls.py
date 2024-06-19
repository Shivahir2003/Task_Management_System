from django.urls import path

from accounts.views import(
    UserLoginView,
    UserSignupView,
    user_logout_view,
    ResetPasswordView,
    profile_view,
    EditProfileView,
)

app_name='accounts'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('signup/',UserSignupView.as_view(),name='signup'),
    path('logout/',user_logout_view,name='logout'),
    path('profile/',profile_view,name='profile'),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset_password')
]