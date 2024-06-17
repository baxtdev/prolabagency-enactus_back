from rest_registration.api.views.change_password import ChangePasswordView
from rest_registration.api.views.login import LoginView,LogoutView
from rest_registration.api.views.profile import ProfileView
from rest_registration.api.views.register import RegisterView

from django.urls import path, re_path, include

from api.users.api import ResetPasswordAPIView,ChekingCodeAPI,GetResetPasswordCodeAPI,RegisterAPIView,GoogleAuthAPIView

# from apps.socialauth.views import GoogleSocialAuthView,FacebookSocialAuthView
urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('profile/',ProfileView.as_view(),name='user-profile'),
    path('logout/',LogoutView.as_view(),name='user-logout'),
    path('reset-password/get-code/<str:email>',GetResetPasswordCodeAPI.as_view(),name='reset-password-get-code'),
    path('reset-password/<int:code>',ResetPasswordAPIView.as_view(),name='reset-password'),
    path('reset-password/chek-code/<int:code>',ChekingCodeAPI.as_view(),name="reset-password-chek-code"),
    path('register/',RegisterAPIView.as_view(),name="user-register"),
    path('google/',GoogleAuthAPIView.as_view(),name="user-auth-google"),
]