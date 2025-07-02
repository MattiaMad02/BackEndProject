from .views import RegisterUser,user_profile
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("profile/", user_profile, name="profile"),
]