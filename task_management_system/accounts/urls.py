from django.urls import path

from accounts.views import UserAuthenticationView

app_name='accounts'
urlpatterns = [
    path('',UserAuthenticationView.as_view()),
    path('login/',UserAuthenticationView.as_view(),name='login'),
    path('signup/',UserAuthenticationView.as_view(),name='signup'),
    path('logout/',UserAuthenticationView.as_view(),name='logout'),
    path('profile/',UserAuthenticationView.as_view(),name='profile'),
    path('edit-profile/',UserAuthenticationView.as_view(),name='edit_profile'),
    path('reset-password/',UserAuthenticationView.as_view(),name='reset_password')
]