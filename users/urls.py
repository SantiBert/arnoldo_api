from django.urls import include, path

from .views import (
    CustomUserView,
    CustomRegisterView,
    LoginView)

urlpatterns = [
    path(
        "auth/login/",
        LoginView.as_view(), 
        name="login"
        ),
    path(
        "auth/register/",
        CustomRegisterView.as_view(), 
        name="register"
        ),
    path(
        "auth/users/",
        CustomUserView.as_view(), 
        name="users"
        ),
]